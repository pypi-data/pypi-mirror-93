import copy
import os
import sys
from datetime import datetime
import argparse
import torch
import torch.optim as optim
import torch.distributed as dist
from torch.cuda.amp import autocast
from torch.cuda.amp import GradScaler
import time
import subprocess
import tempfile
from enum import Enum
from types import FunctionType
from .syszux_annotation import *
from .syszux_log import LOG,getCurrentGitBranch
from .syszux_helper import AverageMeter
try:
    from torch.utils.tensorboard import SummaryWriter
except ImportError:
    LOG.logE("Deepvac has dependency on tensorboard, please install tensorboard first, e.g. [pip3 install tensorboard]", exit=True)

from torch.quantization import QuantStub, DeQuantStub
#fuse model
def fuse4deepvac(civilnet):
    for m in civilnet.modules():
        if not hasattr(m, 'fuse4deepvac'):
            continue
        m.fuse4deepvac()
    if hasattr(civilnet, 'fuse4deepvac'):
        civilnet.fuse4deepvac()

class DeepvacQAT(torch.nn.Module):
    def __init__(self, net2qat):
        super(DeepvacQAT, self).__init__()
        self.quant = QuantStub()
        self.net2qat = fuse4deepvac(net2qat)
        self.dequant = DeQuantStub()

    def forward(self, x):
        x = self.quant(x)
        x = self.net2qat(x)
        x = self.dequant(x)
        return x

#deepvac implemented based on PyTorch Framework
class Deepvac(object):
    def __init__(self, deepvac_config):
        self._mandatory_member = dict()
        self._mandatory_member_name = ['']
        self.input_output = {'input':[], 'output':[]}
        self.conf = deepvac_config
        self.assertInGit()
        #init self.net
        self.initNet()
        self.initNetPost()

    def assertInGit(self):
        if os.environ.get("disable_git"):
            self.branch = "sevice"
            return

        if self.conf.disable_git:
            self.branch = "disable_git"
            return

        self.branch = getCurrentGitBranch()
        if self.branch is None:
            LOG.logE('According to deepvac standard, you must working in a git repo.', exit=True)

        if len(self.branch) < 6:
            LOG.logE('According to deepvac standard, your git branch name is too short: {}'.format(self.branch), exit=True)

        if self.branch.startswith('LTS_'):
            return

        if self.branch.startswith('PROTO_'):
            return

        if self.branch in ['master','main']:
            return

        LOG.logE('According to deepvac standard, git branch name should be master or main, or start from LTS_ or PROTO_: {}'.format(self.branch), exit=True)

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        self.checkIn(name)

    def __delattr__(self, name):
        self.checkOut(name)
        object.__delattr__(self, name)

    def checkIn(self, name):
        if name.startswith('_'):
            return
        self._mandatory_member[name] = None

    def checkOut(self, name):
        if name.startswith('_'):
            return
        del self._mandatory_member[name]

    def auditConfig(self):
        #audit for arch
        for name in self._mandatory_member_name:
            if name not in self._mandatory_member:
                LOG.logE("Error! self.{} must be definded in your subclass.".format(name),exit=True)

        #audit for quantize
        l = [self.conf.static_quantize_dir, self.conf.dynamic_quantize_dir,self.conf.qat_dir]
        l2 = [x for x in l if x]
        if len(l2) > 1:
            LOG.logE("Error: [static_quantize_dir, dynamic_quantize_dir, qat_dir] are exclusive for each other. You can only enable one of them in a train task.")

        #audit for amp
        if self.conf.amp and self.device.type != 'cuda':
            LOG.logE("Error: amp can only be enabled when using cuda device", exit=True)


    def getConf(self):
        return self.conf

    def setInput(self, input):
        if not isinstance(input, list):
            input = [input]

        self.input_output['input'].extend(input)
        self.input_output['output'].clear()

    def addOutput(self, output):
        if not isinstance(output, list):
            output = [output]
        self.input_output['output'].extend(output)

    def getOutput(self):
        self.input_output['input'].clear()
        return self.input_output['output']

    def getTime(self):
        return (str(datetime.now())[:-10]).replace(' ','-').replace(':','-')

    def _parametersInfo(self):
        param_info_list = [p.numel() for p in self.net.parameters() ]
        LOG.logI("self.net has {} parameters.".format(sum(param_info_list)))
        LOG.logI("self.net parameters detail: {}".format(['{}: {}'.format(name, p.numel()) for name, p in self.net.named_parameters()]))

    def initNet(self):
        self.initLog()
        #init self.device
        self.initDevice()
        #init self.net
        self.initNetWithCode()
        #init quantize stuff
        self.initNetWithQuantize()
        #init self.model_dict
        self.initStateDict()
        #just load model after audit
        self.loadStateDict()
        #just print model parameters info
        self._parametersInfo()

    def initNetPost(self):
        self.xb = torch.Tensor().to(self.device)
        self.sample = None

    def initDevice(self):
        #to determine CUDA device, different in DDP
        self.device = torch.device(self.conf.device)

    def initNetWithQuantize(self):
        self.dynamic_quantized_net = None
        self.static_quantized_net = None
        self.static_quantized_net_prepared = None
        self.qat_net_prepared = None
        self.qat_net = None
        if self.conf.qat_dir:
            self.exportQAT(prepare=True)

    def initNetWithCode(self):
        self.net = None
        LOG.logE("You must reimplement initNetWithCode() to initialize self.net", exit=True)

    def initStateDict(self):
        if not self.conf.model_path:
            self.state_dict = None
            LOG.logI("config.model_path not specified, omit the initialization of self.state_dict")
            return
        LOG.logI('Loading State Dict from {}'.format(self.conf.model_path))
        self.state_dict = torch.load(self.conf.model_path, map_location=self.device)
        #remove prefix begin
        prefix = 'module.'
        f = lambda x: x.split(prefix, 1)[-1] if x.startswith(prefix) else x
        if "state_dict" in self.state_dict.keys():
            self.state_dict = {f(key): value for key, value in self.state_dict['state_dict'].items()}
        else:
            self.state_dict = {f(key): value for key, value in self.state_dict.items()}
        #remove prefix end

        # just do audit on model file
        state_dict_keys = set(self.state_dict.keys())
        code_net_keys = set(self.net.state_dict().keys())
        used_keys = code_net_keys & state_dict_keys
        unused_keys = state_dict_keys - code_net_keys
        missing_keys = code_net_keys - state_dict_keys
        LOG.logI('Missing keys:{} | {}'.format(len(missing_keys), missing_keys))
        LOG.logI('Unused keys:{} | {}'.format(len(unused_keys), unused_keys))
        LOG.logI('Used keys:{}'.format(len(used_keys)))
        assert len(used_keys) > 0, 'load NONE from pretrained model'

        if len(missing_keys) > 0:
            LOG.logW("There have missing network parameters, double check if you are using a mismatched trained model.")

    def loadStateDict(self):
        if not self.state_dict:
            LOG.logI("self.state_dict not initialized, omit loadStateDict()")
            return
        self.net.load_state_dict(self.state_dict, strict=False)
        self.net.eval()
        self.net = self.net.to(self.device)

    def initLog(self):
        pass

    def process(self):
        LOG.logE("You must reimplement process() to process self.input_output['input']", exit=True)

    def processSingle(self,sample):
        self.sample = sample
        return self.net(self.sample)

    def __call__(self, input=None):
        if not self.state_dict:
            LOG.logE("self.state_dict not initialized, cannot do predict.", exit=True)

        if input:
            self.setInput(input)

        with torch.no_grad():
            self.process()

        return self.getOutput()

    def saveModel4Libtorch(self, input_net, output_file, mode='trace', input_sample=None):
        LOG.logI("saveModel4Libtorch: {} ...".format(output_file))
        with torch.no_grad():
            if mode == 'trace':
                ts = torch.jit.trace(input_net.eval(), input_sample)
            elif mode == 'script':
                ts = torch.jit.script(input_net.eval())
            else:
                raise Exception('Invalid mode parameter: {}'.format(mode))
        ts.save(output_file)

    def exportTorchViaTrace(self, sample=None, output_trace_file=None):
        if not self.conf.trace_model_dir:
            return
        if sample is None and self.sample is None:
            LOG.logE("either call exportTorchViaTrace and pass value to pamameter sample, or call exportTorchViaTrace in Train mode.", exit=True)

        if sample is not None:
            self.sample = sample

        if output_trace_file is None:
            output_trace_file = self.conf.trace_model_dir

        LOG.logI("config.trace_model_dir found, save trace model to {}...".format(output_trace_file))
        self.saveModel4Libtorch(self.net, output_trace_file, 'trace', self.sample)
        #trace quantized model
        if self.dynamic_quantized_net:
            self.saveModel4Libtorch(self.dynamic_quantized_net, output_trace_file + ".dynamic_quantized", 'trace', self.sample)

        if self.static_quantized_net:
            self.saveModel4Libtorch(self.static_quantized_net, output_trace_file + ".static_quantized", 'trace', self.sample)

        if self.qat_net:
            self.saveModel4Libtorch(self.qat_net, output_trace_file + ".qat_quantized", 'trace', self.sample)

    def exportTorchViaScript(self, output_script_file=None):
        if not self.conf.script_model_dir:
            return

        if output_script_file is None:
            output_script_file = self.conf.script_model_dir

        LOG.logI("config.script_model_dir found, save script model to {}...".format(output_script_file))
        self.saveModel4Libtorch(self.net, output_script_file, 'script')
        #script quantized model
        if self.dynamic_quantized_net:
            self.saveModel4Libtorch(self.dynamic_quantized_net, output_script_file + ".dynamic_quantized", 'script')

        if self.static_quantized_net:
            self.saveModel4Libtorch(self.static_quantized_net, output_script_file + ".static_quantized", 'script')

        if self.qat_net:
            self.saveModel4Libtorch(self.qat_net, output_script_file + ".qat_quantized", 'script')

    def exportNCNN(self, output_ncnn_file=None):
        if not self.conf.ncnn_model_dir:
            return

        if not self.conf.onnx2ncnn:
            LOG.logE("You must set the onnx2ncnn executable program path in config file. If you want to compile onnx2ncnn tools, reference https://github.com/Tencent/ncnn/wiki/how-to-build#build-for-linux-x86 ", exit=True)

        if output_ncnn_file is None:
            output_ncnn_file = self.conf.ncnn_model_dir

        self.ncnn_arch_dir = '{}.param'.format(output_ncnn_file)
        try:
            import onnx
            from onnxsim import simplify
        except:
            LOG.logE("You must install onnx and onnxsim package if you want to convert pytorch to ncnn.")

        if not self.conf.onnx_model_dir:
            f = tempfile.NamedTemporaryFile()
            self.conf.onnx_model_dir = f.name

        self.exportONNX()

        cmd = self.conf.onnx2ncnn + " " + self.conf.onnx_model_dir + " " + self.conf.ncnn_arch_dir + " " + output_ncnn_file
        pd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if pd.stderr.read() != b"":
            LOG.logE(pd.stderr.read() + b". Error occured when export ncnn model. We try to simplify the model first")
            model_op, check_ok = simplify(self.conf.onnx_model_dir, check_n=3, perform_optimization=True, skip_fuse_bn=True,  skip_shape_inference=False)
            onnx.save(model_op, self.conf.onnx_model_dir)
            if not check_ok:
                LOG.logE("Maybe something wrong when simplify the model, we can't guarantee generate model is right")
            else:
                LOG.logI("Simplify model succeed")
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if pd.stderr.read() != b"":
                LOG.logE(pd.stderr.read() + b". we can't guarantee generate model is right")

        LOG.logI("Pytorch model convert to NCNN model succeed, save ncnn param file in {}, save ncnn bin file in {}".format(self.conf.ncnn_arch_dir, output_ncnn_file))

    def exportCoreML(self, output_coreml_file=None):
        if not self.conf.coreml_model_dir:
            return

        if output_coreml_file is None:
            output_coreml_file = self.conf.coreml_model_dir

        try:
            from onnx_coreml import convert
        except:
            LOG.logE("You must install onnx-coreml, coremltools package if you want to convert PyTorch to CoreML model. E.g. pip install --upgrade onnx-coreml coremltools")

        input_names = ["deepvac_in"]
        output_names = ["deepvac_out"]

        if not self.conf.onnx_model_dir:
            f = tempfile.NamedTemporaryFile()
            self.conf.onnx_model_dir = f.name

        #to onnx
        torch.onnx.export(model, self.sample, self.conf.onnx_model_dir, verbose=True, input_names=input_names, output_names=output_names)
        #onnx2coreml
        model_coreml = convert(model=self.conf.onnx_model_dir, preprocessing_args= self.conf.coreml_preprocessing_args, mode=self.conf.coreml_mode, image_input_names=['deepvac_in'],
            class_labels=self.conf.coreml_class_labels, predicted_feature_name='deepvac_out', minimum_ios_deployment_target=self.conf.minimum_ios_deployment_target)

        # Save the CoreML model
        coreml_model.save(output_coreml_file)

    def exportONNX(self, output_onnx_file=None):
        if not self.conf.onnx_model_dir:
            return
        if output_onnx_file is None:
            output_onnx_file = self.onnx_model_dir
        else:
            self.onnx_model_dir = output_onnx_file

        torch.onnx._export(self.net, self.sample, output_onnx_file, export_params=True)
        LOG.logI("Pytorch model convert to ONNX model succeed, save model in {}".format(output_onnx_file))

    def exportDynamicQuant(self, output_quant_file=None):
        if not self.conf.dynamic_quantize_dir:
            return

        if output_quant_file is None:
            output_quant_file = self.conf.dynamic_quantize_dir

        self.dynamic_quantized_net = torch.quantization.quantize_dynamic(self.net)
        self.dynamic_quantized_net.eval()
        torch.save(self.dynamic_quantized_net.state_dict(), output_quant_file)
        LOG.logI("Pytorch model dynamic quantize succeed, save model in {}".format(output_quant_file))

    def exportStaticQuant(self, output_quant_file=None, prepare=False):
        if not self.conf.static_quantize_dir:
            return

        if prepare:
            LOG.logI("You have enabled static quantization, this step is only for prepare.")

            if self.static_quantized_net_prepared:
                LOG.logE("Error: You have already prepared the model for static quantization.", exit=True)

            backend = 'fbgemm'
            if self.conf.quantize_backend:
                backend = self.conf.quantize_backend

            self.static_quantized_net_prepared = copy.deepcopy(self.net) if self.conf.modules_to_fuse is None else torch.quantization.fuse_modules(self.net, self.conf.modules_to_fuse)
            self.static_quantized_net_prepared.qconfig = torch.quantization.get_default_qconfig(backend)
            torch.quantization.prepare(self.static_quantized_net_prepared, inplace=True)
            self.static_quantized_net_prepared.eval()
            return

        if self.static_quantized_net_prepared is None:
            LOG.logE("Error: You haven't prepared the model for static quantization. call exportStaticQuant(prepare=True) first.",exit=True)

        if output_quant_file is None:
            output_quant_file = self.conf.static_quantize_dir

        self.static_quantized_net = torch.quantization.convert(self.static_quantized_net_prepared)
        #important to recover to None
        self.static_quantized_net_prepared = None
        LOG.logI("Pytorch model static quantize succeed, save model in {}".format(output_quant_file))
        torch.save(self.static_quantized_net.state_dict(), output_quant_file)

    def exportQAT(self, output_quant_file=None, prepare=False):
        if not self.conf.qat_dir:
            return

        if prepare:
            LOG.logI("You have enabled QAT, this step is only for prepare.")

            if self.qat_net_prepared:
                LOG.logE("Error: You have already prepared the model for QAT.", exit=True)

            backend = 'fbgemm'
            if self.conf.quantize_backend:
                backend = self.conf.quantize_backend
            
            self.qat_net_prepared = self.net if self.conf.modules_to_fuse is None else torch.quantization.fuse_modules(self.net, self.conf.modules_to_fuse)
            self.qat_net_prepared.qconfig = torch.quantization.get_default_qat_qconfig(backend)
            torch.quantization.prepare_qat(self.qat_net_prepared, inplace=True)
            #after this, train net will be transfered to QAT !
            self.net = self.qat_net_prepared
            return

        if self.qat_net_prepared is None:
            LOG.logE("Error: You haven't prepared the model for QAT. call exportQAT(prepare=True) first.",exit=True)

        if output_quant_file is None:
            output_quant_file = self.conf.qat_dir

        is_train = self.net.training
        #to eval mode temporary
        if is_train:
            self.net.eval()
        self.qat_net = torch.quantization.convert(self.net)
        LOG.logI("Pytorch model QAT quantize succeed, save model in {}".format(output_quant_file))
        torch.save(self.qat_net.state_dict(), output_quant_file)
        #back to train mode.
        if is_train:
            self.net.train()

    def loadDB(self, db_path):
        self.xb = torch.load(db_path).to(self.device)

    def addEmb2DB(self, emb):
        self.xb = torch.cat((self.xb, emb))

    def saveDB(self, db_path):
        torch.save(self.xb, db_path)

    def search(self, xq, k=1):
        D = []
        I = []
        if k < 1 or k > 10:
            LOG.logE('illegal nearest neighbors parameter k(1 ~ 10): {}'.format(k))
            return D, I

        distance = torch.norm(self.xb - xq, dim=1)
        for i in range(k):
            values, indices = distance.kthvalue(i+1)
            D.append(values.item())
            I.append(indices.item())
        return D, I

class DeepvacTrain(Deepvac):
    def __init__(self, deepvac_config):
        super(DeepvacTrain,self).__init__(deepvac_config)
        self.initTrainParameters()
        self.initTrainContext()

    def setTrainContext(self):
        self.is_train = True
        self.is_val = False
        self.phase = 'TRAIN'
        self.dataset = self.train_dataset
        self.loader = self.train_loader
        self.batch_size = self.conf.train.batch_size
        self.net.train()
        if self.qat_net_prepared:
            self.qat_net_prepared.train()

    def setValContext(self):
        self.is_train = False
        self.is_val = True
        self.phase = 'VAL'
        self.dataset = self.val_dataset
        self.loader = self.val_loader
        self.batch_size = self.conf.val.batch_size
        self.net.eval()
        if self.qat_net_prepared:
            self.qat_net_prepared.eval()

    def initTrainContext(self):
        self.scheduler = None
        self.initOutputDir()
        self.initSummaryWriter()
        self.initCriterion()
        self.initOptimizer()
        self.initScheduler()
        self.initCheckpoint()
        self.initTrainLoader()
        self.initValLoader()

    def initTrainParameters(self):
        self.dataset = None
        self.loader = None
        self.target = None
        self.epoch = 0
        self.step = 0
        self.iter = 0
        # Creates a GradScaler once at the beginning of training.
        self.scaler = GradScaler()
        self.train_time = AverageMeter()
        self.load_data_time = AverageMeter()
        self.data_cpu2gpu_time = AverageMeter()
        self._mandatory_member_name = ['train_dataset','val_dataset','train_loader','val_loader','net','criterion','optimizer']

    def initOutputDir(self):
        if self.conf.output_dir != 'output' or self.conf.output_dir != './output':
            LOG.logW("According deepvac standard, you should save model files to [output] directory.")

        self.output_dir = '{}/{}'.format(self.conf.output_dir, self.branch)
        LOG.logI('model save dir: {}'.format(self.output_dir))
        #for DDP race condition
        os.makedirs(self.output_dir, exist_ok=True)

    def initSummaryWriter(self):
        event_dir = "{}/{}".format(self.conf.log_dir, self.branch)
        self.writer = SummaryWriter(event_dir)
        if not self.conf.tensorboard_port:
            return
        from tensorboard import program
        tensorboard = program.TensorBoard()
        self.conf.tensorboard_ip = '0.0.0.0' if self.conf.tensorboard_ip is None else self.conf.tensorboard_ip
        tensorboard.configure(argv=[None, '--host', str(self.conf.tensorboard_ip),'--logdir', event_dir, "--port", str(self.conf.tensorboard_port)])
        try:
            url = tensorboard.launch()
            LOG.logI('Tensorboard at {} '.format(url))
        except Exception as e:
            LOG.logE(e.msg)

    def initCriterion(self):
        self.criterion = torch.nn.CrossEntropyLoss()
        LOG.logW("You should reimplement initCriterion() to initialize self.criterion, unless CrossEntropyLoss() is exactly what you need")

    def initCheckpoint(self):
        if not self.conf.checkpoint_suffix or self.conf.checkpoint_suffix == "":
            LOG.logI('Omit the checkpoint file since not specified...')
            return
        LOG.logI('Load checkpoint from {} folder'.format(self.output_dir))
        self.net.load_state_dict(torch.load(self.output_dir+'/model__{}'.format(self.conf.checkpoint_suffix), map_location=self.device))
        state_dict = torch.load(self.output_dir+'/checkpoint__{}'.format(self.conf.checkpoint_suffix), map_location=self.device)
        self.optimizer.load_state_dict(state_dict['optimizer'])
        if self.scheduler:
            self.scheduler.load_state_dict(state_dict['scheduler'])
        if self.conf.amp:
            LOG.logI("Will load scaler from checkpoint since you enabled amp, make sure the checkpoint was saved with amp enabled.")
            try:
                self.scaler.load_state_dict(state_dict["scaler"])
            except:
                LOG.logI("checkpoint was saved without amp enabled, so use fresh GradScaler instead.")
                self.scaler = GradScaler()

        self.epoch = state_dict['epoch']

    def initScheduler(self):
        if isinstance(self.conf.lr_step, list):
            self.scheduler = torch.optim.lr_scheduler.MultiStepLR(self.optimizer, self.conf.lr_step,self.conf.lr_factor)
        elif isinstance(self.conf.lr_step, FunctionType):
            self.scheduler = torch.optim.lr_scheduler.LambdaLR(self.optimizer, lr_lambda=self.conf.lr_step)
        else:
            self.scheduler = torch.optim.lr_scheduler.StepLR(self.optimizer, self.conf.lr_step,self.conf.lr_factor)
        LOG.logW("You should reimplement initScheduler() to initialize self.scheduler, unless lr_scheduler.StepLR() or lr_scheduler.MultiStepLR() is exactly what you need")

    def initTrainLoader(self):
        self.train_loader = None
        LOG.logE("You must reimplement initTrainLoader() to initialize self.train_loader", exit=True)

    def initValLoader(self):
        self.val_loader = None
        LOG.logE("You must reimplement initTrainLoader() to initialize self.val_loader", exit=True)

    def initOptimizer(self):
        self.initSgdOptimizer()
        LOG.logW("You should reimplement initOptimizer() to initialize self.optimizer, unless SGD is exactly what you need")

    def initSgdOptimizer(self):
        self.optimizer = optim.SGD(self.net.parameters(),
            lr=self.conf.lr,
            momentum=self.conf.momentum,
            weight_decay=self.conf.weight_decay,
            nesterov=self.conf.nesterov
        )

    def initAdamOptimizer(self):
        self.optimizer = optim.Adam(
            self.net.parameters(),
            lr=self.conf.lr,
        )
        for group in self.optimizer.param_groups:
            group.setdefault('initial_lr', group['lr'])

    def initRmspropOptimizer(self):
        self.optimizer = optim.RMSprop(
            self.net.parameters(),
            lr=self.conf.lr,
            momentum=self.conf.momentum,
            weight_decay=self.conf.weight_decay,
            # alpha=self.conf.rmsprop_alpha,
            # centered=self.conf.rmsprop_centered
        )

    def addScalar(self, tag, value, step):
        self.writer.add_scalar(tag, value, step)

    def addImage(self, tag, image, step):
        self.writer.add_image(tag, image, step)

    @syszux_once
    def addGraph(self, input):
        self.writer.add_graph(self.net, input)

    @syszux_once
    def smokeTestForExport3rd(self):
        #exportNCNN must before exportONNX
        self.exportONNX()
        self.exportNCNN()
        self.exportCoreML()
        #whether export TorchScript via trace, only here we can get self.sample
        self.exportTorchViaTrace()
        #compile pytorch state dict to TorchScript
        self.exportTorchViaScript()
        self.exportDynamicQuant()
        self.exportStaticQuant()

    def earlyIter(self):
        start = time.time()
        self.sample = self.sample.to(self.device)
        self.target = self.target.to(self.device)
        if not self.is_train:
            return
        self.data_cpu2gpu_time.update(time.time() - start)
        try:
            self.addGraph(self.sample)
        except:
            LOG.logW("Tensorboard addGraph failed. You network foward may have more than one parameters?")
            LOG.logW("Seems you need reimplement preIter function.")

    def preIter(self):
        pass

    def postIter(self):
        pass

    def preEpoch(self):
        pass

    def postEpoch(self):
        pass

    def doForward(self):
        self.output = self.net(self.sample)

    def doCalibrate(self):
        if not self.conf.static_quantize_dir:
            return
        if self.static_quantized_net_prepared is None:
            LOG.logE("Error: You haven't prepared the model for static quantization. call exportStaticQuant(prepare=True) first.",exit=True)

        self.static_quantized_net_prepared(self.sample)

    def doLoss(self):
        self.loss = self.criterion(self.output, self.target)

    def doBackward(self):
        if self.conf.amp:
            self.scaler.scale(self.loss).backward()
        else:
            self.loss.backward()

    def doOptimize(self):
        if self.iter % self.conf.nominal_batch_factor != 0:
            return
        if self.conf.amp:
            self.scaler.step(self.optimizer)
            self.scaler.update()
        else:
            self.optimizer.step()
        self.optimizer.zero_grad()

    def doLog(self):
        if self.step % self.conf.log_every != 0:
            return
        self.addScalar('{}/Loss'.format(self.phase), self.loss.item(), self.iter)
        self.addScalar('{}/LoadDataTime(secs/batch)'.format(self.phase), self.load_data_time.val, self.iter)
        self.addScalar('{}/DataCpu2GpuTime(secs/batch)'.format(self.phase), self.data_cpu2gpu_time.val, self.iter)
        self.addScalar('{}/TrainTime(secs/batch)'.format(self.phase), self.train_time.val, self.iter)
        LOG.logI('{}: [{}][{}/{}] [Loss:{}  Lr:{}]'.format(self.phase, self.epoch, self.step, self.loader_len,self.loss.item(),self.optimizer.param_groups[0]['lr']))

    def saveState(self, current_time):
        file_partial_name = '{}__acc_{}__epoch_{}__step_{}__lr_{}'.format(current_time, self.accuracy, self.epoch, self.step, self.optimizer.param_groups[0]['lr'])
        state_file = '{}/model__{}.pth'.format(self.output_dir, file_partial_name)
        checkpoint_file = '{}/checkpoint__{}.pth'.format(self.output_dir, file_partial_name)
        output_trace_file = '{}/trace__{}.pt'.format(self.output_dir, file_partial_name)
        output_script_file = '{}/script__{}.pt'.format(self.output_dir, file_partial_name)
        output_onnx_file = '{}/onnx__{}.onnx'.format(self.output_dir, file_partial_name)
        output_ncnn_file = '{}/ncnn__{}.bin'.format(self.output_dir, file_partial_name)
        output_coreml_file = '{}/coreml__{}.mlmodel'.format(self.output_dir, file_partial_name)
        output_dynamic_quant_file = '{}/dquant__{}.pt'.format(self.output_dir, file_partial_name)
        output_static_quant_file = '{}/squant__{}.pt'.format(self.output_dir, file_partial_name)
        output_qat_file = '{}/qat__{}.pt'.format(self.output_dir, file_partial_name)
        #save state_dict
        torch.save(self.net.state_dict(), state_file)
        #save checkpoint
        torch.save({
            'optimizer': self.optimizer.state_dict(),
            'epoch': self.epoch,
            'scheduler': self.scheduler.state_dict() if self.scheduler else None,
            'scaler': self.scaler.state_dict() if self.conf.amp else None},  checkpoint_file)

        #convert for quantize, must before trace and script!!!
        self.exportDynamicQuant(output_dynamic_quant_file)
        self.exportStaticQuant(output_quant_file=output_static_quant_file)
        self.exportQAT(output_quant_file=output_qat_file)
        #save pt via trace
        self.exportTorchViaTrace(self.sample, output_trace_file)
        #save pt vida script
        self.exportTorchViaScript(output_script_file)
        #save onnx
        self.exportONNX(output_onnx_file)
        #save ncnn
        self.exportNCNN(output_ncnn_file)
        #save coreml
        self.exportCoreML(output_coreml_file)
        #tensorboard
        self.addScalar('{}/Accuracy'.format(self.phase), self.accuracy, self.iter)

    def processTrain(self):
        self.setTrainContext()
        self.step = 0
        LOG.logI('Phase {} started...'.format(self.phase))
        self.loader_len = len(self.loader)
        save_every = self.loader_len//self.conf.save_num
        save_list = list(range(0, self.loader_len + 1, save_every ))
        self.save_list = save_list[1:-1]
        LOG.logI('Model will be saved on step {} and the epoch end.'.format(self.save_list))
        self.addScalar('{}/LR'.format(self.phase), self.optimizer.param_groups[0]['lr'], self.epoch)
        self.preEpoch()
        self.train_time.reset()
        self.load_data_time.reset()
        self.data_cpu2gpu_time.reset()

        start = time.time()
        for i, (sample, target) in enumerate(self.loader):
            self.load_data_time.update(time.time() - start)
            self.step = i
            self.target = target
            self.sample = sample
            self.preIter()
            self.earlyIter()
            with autocast(enabled=self.conf.amp if self.conf.amp else False):
                self.doForward()
                self.doLoss()
            self.doBackward()
            self.doOptimize()
            self.doLog()
            self.postIter()
            self.iter += 1
            self.train_time.update(time.time() - start)
            if self.step in self.save_list:
                self.processVal()
                self.setTrainContext()
            start = time.time()

        self.addScalar('{}/TrainTime(hours/epoch)'.format(self.phase), round(self.train_time.sum / 3600, 2), self.epoch)
        self.addScalar('{}/AverageBatchTrainTime(secs/epoch)'.format(self.phase), self.train_time.avg, self.epoch)
        self.addScalar('{}/AverageBatchLoadDataTime(secs/epoch)'.format(self.phase), self.load_data_time.avg, self.epoch)
        self.addScalar('{}/AverageBatchDataCpu2GpuTime(secs/epoch)'.format(self.phase), self.data_cpu2gpu_time.avg, self.epoch)

        self.postEpoch()
        if self.scheduler:
            self.scheduler.step()

    def processVal(self, smoke=False):
        self.setValContext()
        LOG.logI('Phase {} started...'.format(self.phase))
        #prepare the static quant
        self.exportStaticQuant(prepare=True)
        with torch.no_grad():
            self.preEpoch()
            for i, (sample, target) in enumerate(self.loader):
                self.target = target
                self.sample = sample
                self.preIter()
                self.earlyIter()
                self.doForward()
                #calibrate only for quantization.
                self.doCalibrate()
                self.doLoss()
                self.smokeTestForExport3rd()
                self.postIter()
                if smoke:
                    return
                LOG.logI('{}: [{}][{}/{}]'.format(self.phase, self.epoch, i, len(self.loader)))
            self.postEpoch()
        self.saveState(self.getTime())

    def processAccept(self):
        self.setValContext()

    def process(self):
        self.auditConfig()
        self.iter = 0
        epoch_start = self.epoch
        self.processVal(smoke=True)
        self.optimizer.zero_grad()
        for epoch in range(epoch_start, self.conf.epoch_num):
            self.epoch = epoch
            LOG.logI('Epoch {} started...'.format(self.epoch))
            self.processTrain()
            self.processVal()
            self.processAccept()

    def __call__(self):
        self.process()

class DeepvacDDP(DeepvacTrain):
    def __init__(self, deepvac_config):
        super(DeepvacDDP,self).__init__(deepvac_config)
        assert self.train_sampler is not None, "You should define self.train_sampler in DDP mode."

    def initDevice(self):
        super(DeepvacDDP, self).initDevice()
        parser = argparse.ArgumentParser(description='DeepvacDDP')
        parser.add_argument("--gpu", default=-1, type=int, help="gpu")
        parser.add_argument('--rank', default=-1, type=int, help='node rank for distributed training')
        self.args = parser.parse_args()
        self.map_location = {'cuda:%d' % 0: 'cuda:%d' % self.args.rank}
        #in DDP, device may come from command line
        if self.args.gpu:
            self.device = torch.device(self.args.gpu)

        #os.environ["CUDA_VISIBLE_DEVICES"] = "{}".format(self.args.gpu)
        torch.cuda.set_device(self.args.gpu)

    def initDDP(self):
        LOG.logI("Start dist.init_process_group {} {}@{} on {}".format(self.conf.dist_url, self.args.rank, self.conf.world_size - 1, self.args.gpu))
        dist.init_process_group(backend='nccl', init_method=self.conf.dist_url, world_size=self.conf.world_size, rank=self.args.rank)
        #torch.cuda.set_device(self.args.gpu)
        self.net = torch.nn.parallel.DistributedDataParallel(self.net, device_ids=[self.args.gpu])
        LOG.logI("Finish dist.init_process_group {} {}@{} on {}".format(self.conf.dist_url, self.args.rank, self.conf.world_size - 1, self.args.gpu))

    def initTrainContext(self):
        self.initDDP()
        super(DeepvacDDP,self).initTrainContext()

    def initSummaryWriter(self):
        if self.args.rank != 0:
            return
        super(DeepvacDDP, self).initSummaryWriter()

    def preEpoch(self):
        self.train_sampler.set_epoch(self.epoch)

    def smokeTestForExport3rd(self):
        if self.args.rank != 0:
            return
        super(DeepvacDDP, self).smokeTestForExport3rd()

    def saveState(self, time):
        if self.args.rank != 0:
            return
        super(DeepvacDDP, self).saveState(self.getTime())

    def addScalar(self, tag, value, step):
        if self.args.rank != 0:
            return
        super(DeepvacDDP, self).addScalar(tag, value, step)

    def addImage(self, tag, image, step):
        if self.args.rank != 0:
            return
        super(DeepvacDDP, self).addImage(tag, image, step)

    @syszux_once
    def addGraph(self, input):
        if self.args.rank != 0:
            return
        self.writer.add_graph(self.net, input)

if __name__ == "__main__":
    from config import config as deepvac_config
    vac = Deepvac(deepvac_config)
    vac()

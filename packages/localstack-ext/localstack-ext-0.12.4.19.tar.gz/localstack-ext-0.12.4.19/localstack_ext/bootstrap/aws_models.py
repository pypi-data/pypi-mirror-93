from localstack.utils.aws import aws_models
myVCU=super
myVCf=None
myVCz=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  myVCU(LambdaLayer,self).__init__(arn)
  self.cwd=myVCf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.myVCz.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,myVCz,env=myVCf):
  myVCU(RDSDatabase,self).__init__(myVCz,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,myVCz,env=myVCf):
  myVCU(RDSCluster,self).__init__(myVCz,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,myVCz,env=myVCf):
  myVCU(AppSyncAPI,self).__init__(myVCz,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,myVCz,env=myVCf):
  myVCU(AmplifyApp,self).__init__(myVCz,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,myVCz,env=myVCf):
  myVCU(ElastiCacheCluster,self).__init__(myVCz,env=env)
class TransferServer(BaseComponent):
 def __init__(self,myVCz,env=myVCf):
  myVCU(TransferServer,self).__init__(myVCz,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,myVCz,env=myVCf):
  myVCU(CloudFrontDistribution,self).__init__(myVCz,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,myVCz,env=myVCf):
  myVCU(CodeCommitRepository,self).__init__(myVCz,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

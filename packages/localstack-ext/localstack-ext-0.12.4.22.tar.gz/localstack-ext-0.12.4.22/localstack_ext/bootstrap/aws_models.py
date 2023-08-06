from localstack.utils.aws import aws_models
KBGNA=super
KBGNQ=None
KBGNP=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  KBGNA(LambdaLayer,self).__init__(arn)
  self.cwd=KBGNQ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.KBGNP.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,KBGNP,env=KBGNQ):
  KBGNA(RDSDatabase,self).__init__(KBGNP,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,KBGNP,env=KBGNQ):
  KBGNA(RDSCluster,self).__init__(KBGNP,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,KBGNP,env=KBGNQ):
  KBGNA(AppSyncAPI,self).__init__(KBGNP,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,KBGNP,env=KBGNQ):
  KBGNA(AmplifyApp,self).__init__(KBGNP,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,KBGNP,env=KBGNQ):
  KBGNA(ElastiCacheCluster,self).__init__(KBGNP,env=env)
class TransferServer(BaseComponent):
 def __init__(self,KBGNP,env=KBGNQ):
  KBGNA(TransferServer,self).__init__(KBGNP,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,KBGNP,env=KBGNQ):
  KBGNA(CloudFrontDistribution,self).__init__(KBGNP,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,KBGNP,env=KBGNQ):
  KBGNA(CodeCommitRepository,self).__init__(KBGNP,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

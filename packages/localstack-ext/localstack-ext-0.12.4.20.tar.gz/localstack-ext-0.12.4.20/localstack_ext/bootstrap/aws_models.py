from localstack.utils.aws import aws_models
ndsYl=super
ndsYf=None
ndsYA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  ndsYl(LambdaLayer,self).__init__(arn)
  self.cwd=ndsYf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.ndsYA.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,ndsYA,env=ndsYf):
  ndsYl(RDSDatabase,self).__init__(ndsYA,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,ndsYA,env=ndsYf):
  ndsYl(RDSCluster,self).__init__(ndsYA,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,ndsYA,env=ndsYf):
  ndsYl(AppSyncAPI,self).__init__(ndsYA,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,ndsYA,env=ndsYf):
  ndsYl(AmplifyApp,self).__init__(ndsYA,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,ndsYA,env=ndsYf):
  ndsYl(ElastiCacheCluster,self).__init__(ndsYA,env=env)
class TransferServer(BaseComponent):
 def __init__(self,ndsYA,env=ndsYf):
  ndsYl(TransferServer,self).__init__(ndsYA,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,ndsYA,env=ndsYf):
  ndsYl(CloudFrontDistribution,self).__init__(ndsYA,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,ndsYA,env=ndsYf):
  ndsYl(CodeCommitRepository,self).__init__(ndsYA,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

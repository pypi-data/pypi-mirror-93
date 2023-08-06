from localstack.utils.aws import aws_models
wYzqj=super
wYzqx=None
wYzqT=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  wYzqj(LambdaLayer,self).__init__(arn)
  self.cwd=wYzqx
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.wYzqT.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,wYzqT,env=wYzqx):
  wYzqj(RDSDatabase,self).__init__(wYzqT,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,wYzqT,env=wYzqx):
  wYzqj(RDSCluster,self).__init__(wYzqT,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,wYzqT,env=wYzqx):
  wYzqj(AppSyncAPI,self).__init__(wYzqT,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,wYzqT,env=wYzqx):
  wYzqj(AmplifyApp,self).__init__(wYzqT,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,wYzqT,env=wYzqx):
  wYzqj(ElastiCacheCluster,self).__init__(wYzqT,env=env)
class TransferServer(BaseComponent):
 def __init__(self,wYzqT,env=wYzqx):
  wYzqj(TransferServer,self).__init__(wYzqT,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,wYzqT,env=wYzqx):
  wYzqj(CloudFrontDistribution,self).__init__(wYzqT,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,wYzqT,env=wYzqx):
  wYzqj(CodeCommitRepository,self).__init__(wYzqT,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

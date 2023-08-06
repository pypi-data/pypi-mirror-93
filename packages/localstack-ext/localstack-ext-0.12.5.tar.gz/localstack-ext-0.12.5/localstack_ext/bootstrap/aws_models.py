from localstack.utils.aws import aws_models
MaJWX=super
MaJWw=None
MaJWm=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  MaJWX(LambdaLayer,self).__init__(arn)
  self.cwd=MaJWw
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.MaJWm.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,MaJWm,env=MaJWw):
  MaJWX(RDSDatabase,self).__init__(MaJWm,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,MaJWm,env=MaJWw):
  MaJWX(RDSCluster,self).__init__(MaJWm,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,MaJWm,env=MaJWw):
  MaJWX(AppSyncAPI,self).__init__(MaJWm,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,MaJWm,env=MaJWw):
  MaJWX(AmplifyApp,self).__init__(MaJWm,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,MaJWm,env=MaJWw):
  MaJWX(ElastiCacheCluster,self).__init__(MaJWm,env=env)
class TransferServer(BaseComponent):
 def __init__(self,MaJWm,env=MaJWw):
  MaJWX(TransferServer,self).__init__(MaJWm,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,MaJWm,env=MaJWw):
  MaJWX(CloudFrontDistribution,self).__init__(MaJWm,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,MaJWm,env=MaJWw):
  MaJWX(CodeCommitRepository,self).__init__(MaJWm,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

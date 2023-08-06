from localstack.utils.aws import aws_models
pdNaG=super
pdNaw=None
pdNaz=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  pdNaG(LambdaLayer,self).__init__(arn)
  self.cwd=pdNaw
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.pdNaz.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,pdNaz,env=pdNaw):
  pdNaG(RDSDatabase,self).__init__(pdNaz,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,pdNaz,env=pdNaw):
  pdNaG(RDSCluster,self).__init__(pdNaz,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,pdNaz,env=pdNaw):
  pdNaG(AppSyncAPI,self).__init__(pdNaz,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,pdNaz,env=pdNaw):
  pdNaG(AmplifyApp,self).__init__(pdNaz,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,pdNaz,env=pdNaw):
  pdNaG(ElastiCacheCluster,self).__init__(pdNaz,env=env)
class TransferServer(BaseComponent):
 def __init__(self,pdNaz,env=pdNaw):
  pdNaG(TransferServer,self).__init__(pdNaz,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,pdNaz,env=pdNaw):
  pdNaG(CloudFrontDistribution,self).__init__(pdNaz,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,pdNaz,env=pdNaw):
  pdNaG(CodeCommitRepository,self).__init__(pdNaz,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

from localstack.utils.aws import aws_models
TcfBI=super
TcfBF=None
TcfBj=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  TcfBI(LambdaLayer,self).__init__(arn)
  self.cwd=TcfBF
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.TcfBj.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,TcfBj,env=TcfBF):
  TcfBI(RDSDatabase,self).__init__(TcfBj,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,TcfBj,env=TcfBF):
  TcfBI(RDSCluster,self).__init__(TcfBj,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,TcfBj,env=TcfBF):
  TcfBI(AppSyncAPI,self).__init__(TcfBj,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,TcfBj,env=TcfBF):
  TcfBI(AmplifyApp,self).__init__(TcfBj,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,TcfBj,env=TcfBF):
  TcfBI(ElastiCacheCluster,self).__init__(TcfBj,env=env)
class TransferServer(BaseComponent):
 def __init__(self,TcfBj,env=TcfBF):
  TcfBI(TransferServer,self).__init__(TcfBj,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,TcfBj,env=TcfBF):
  TcfBI(CloudFrontDistribution,self).__init__(TcfBj,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,TcfBj,env=TcfBF):
  TcfBI(CodeCommitRepository,self).__init__(TcfBj,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

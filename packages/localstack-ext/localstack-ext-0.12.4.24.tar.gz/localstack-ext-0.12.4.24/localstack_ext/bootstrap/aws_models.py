from localstack.utils.aws import aws_models
QMeGl=super
QMeGA=None
QMeGX=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  QMeGl(LambdaLayer,self).__init__(arn)
  self.cwd=QMeGA
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.QMeGX.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,QMeGX,env=QMeGA):
  QMeGl(RDSDatabase,self).__init__(QMeGX,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,QMeGX,env=QMeGA):
  QMeGl(RDSCluster,self).__init__(QMeGX,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,QMeGX,env=QMeGA):
  QMeGl(AppSyncAPI,self).__init__(QMeGX,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,QMeGX,env=QMeGA):
  QMeGl(AmplifyApp,self).__init__(QMeGX,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,QMeGX,env=QMeGA):
  QMeGl(ElastiCacheCluster,self).__init__(QMeGX,env=env)
class TransferServer(BaseComponent):
 def __init__(self,QMeGX,env=QMeGA):
  QMeGl(TransferServer,self).__init__(QMeGX,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,QMeGX,env=QMeGA):
  QMeGl(CloudFrontDistribution,self).__init__(QMeGX,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,QMeGX,env=QMeGA):
  QMeGl(CodeCommitRepository,self).__init__(QMeGX,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

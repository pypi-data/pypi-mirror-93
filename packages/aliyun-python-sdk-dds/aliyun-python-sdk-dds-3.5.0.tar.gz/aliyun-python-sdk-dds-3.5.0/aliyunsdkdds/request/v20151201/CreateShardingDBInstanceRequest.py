# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkdds.endpoint import endpoint_data

class CreateShardingDBInstanceRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Dds', '2015-12-01', 'CreateShardingDBInstance','Dds')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_ClientToken(self):
		return self.get_query_params().get('ClientToken')

	def set_ClientToken(self,ClientToken):
		self.add_query_param('ClientToken',ClientToken)

	def get_EngineVersion(self):
		return self.get_query_params().get('EngineVersion')

	def set_EngineVersion(self,EngineVersion):
		self.add_query_param('EngineVersion',EngineVersion)

	def get_NetworkType(self):
		return self.get_query_params().get('NetworkType')

	def set_NetworkType(self,NetworkType):
		self.add_query_param('NetworkType',NetworkType)

	def get_ReplicaSets(self):
		return self.get_query_params().get('ReplicaSet')

	def set_ReplicaSets(self, ReplicaSets):
		for depth1 in range(len(ReplicaSets)):
			if ReplicaSets[depth1].get('ReadonlyReplicas') is not None:
				self.add_query_param('ReplicaSet.' + str(depth1 + 1) + '.ReadonlyReplicas', ReplicaSets[depth1].get('ReadonlyReplicas'))
			if ReplicaSets[depth1].get('Storage') is not None:
				self.add_query_param('ReplicaSet.' + str(depth1 + 1) + '.Storage', ReplicaSets[depth1].get('Storage'))
			if ReplicaSets[depth1].get('Class') is not None:
				self.add_query_param('ReplicaSet.' + str(depth1 + 1) + '.Class', ReplicaSets[depth1].get('Class'))

	def get_StorageEngine(self):
		return self.get_query_params().get('StorageEngine')

	def set_StorageEngine(self,StorageEngine):
		self.add_query_param('StorageEngine',StorageEngine)

	def get_SecurityToken(self):
		return self.get_query_params().get('SecurityToken')

	def set_SecurityToken(self,SecurityToken):
		self.add_query_param('SecurityToken',SecurityToken)

	def get_Engine(self):
		return self.get_query_params().get('Engine')

	def set_Engine(self,Engine):
		self.add_query_param('Engine',Engine)

	def get_DBInstanceDescription(self):
		return self.get_query_params().get('DBInstanceDescription')

	def set_DBInstanceDescription(self,DBInstanceDescription):
		self.add_query_param('DBInstanceDescription',DBInstanceDescription)

	def get_Period(self):
		return self.get_query_params().get('Period')

	def set_Period(self,Period):
		self.add_query_param('Period',Period)

	def get_RestoreTime(self):
		return self.get_query_params().get('RestoreTime')

	def set_RestoreTime(self,RestoreTime):
		self.add_query_param('RestoreTime',RestoreTime)

	def get_ResourceOwnerAccount(self):
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def get_SrcDBInstanceId(self):
		return self.get_query_params().get('SrcDBInstanceId')

	def set_SrcDBInstanceId(self,SrcDBInstanceId):
		self.add_query_param('SrcDBInstanceId',SrcDBInstanceId)

	def get_OwnerAccount(self):
		return self.get_query_params().get('OwnerAccount')

	def set_OwnerAccount(self,OwnerAccount):
		self.add_query_param('OwnerAccount',OwnerAccount)

	def get_ConfigServers(self):
		return self.get_query_params().get('ConfigServer')

	def set_ConfigServers(self, ConfigServers):
		for depth1 in range(len(ConfigServers)):
			if ConfigServers[depth1].get('Storage') is not None:
				self.add_query_param('ConfigServer.' + str(depth1 + 1) + '.Storage', ConfigServers[depth1].get('Storage'))
			if ConfigServers[depth1].get('Class') is not None:
				self.add_query_param('ConfigServer.' + str(depth1 + 1) + '.Class', ConfigServers[depth1].get('Class'))

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_SecurityIPList(self):
		return self.get_query_params().get('SecurityIPList')

	def set_SecurityIPList(self,SecurityIPList):
		self.add_query_param('SecurityIPList',SecurityIPList)

	def get_VSwitchId(self):
		return self.get_query_params().get('VSwitchId')

	def set_VSwitchId(self,VSwitchId):
		self.add_query_param('VSwitchId',VSwitchId)

	def get_Mongoss(self):
		return self.get_query_params().get('Mongos')

	def set_Mongoss(self, Mongoss):
		for depth1 in range(len(Mongoss)):
			if Mongoss[depth1].get('Class') is not None:
				self.add_query_param('Mongos.' + str(depth1 + 1) + '.Class', Mongoss[depth1].get('Class'))

	def get_AccountPassword(self):
		return self.get_query_params().get('AccountPassword')

	def set_AccountPassword(self,AccountPassword):
		self.add_query_param('AccountPassword',AccountPassword)

	def get_AutoRenew(self):
		return self.get_query_params().get('AutoRenew')

	def set_AutoRenew(self,AutoRenew):
		self.add_query_param('AutoRenew',AutoRenew)

	def get_VpcId(self):
		return self.get_query_params().get('VpcId')

	def set_VpcId(self,VpcId):
		self.add_query_param('VpcId',VpcId)

	def get_ZoneId(self):
		return self.get_query_params().get('ZoneId')

	def set_ZoneId(self,ZoneId):
		self.add_query_param('ZoneId',ZoneId)

	def get_ProtocolType(self):
		return self.get_query_params().get('ProtocolType')

	def set_ProtocolType(self,ProtocolType):
		self.add_query_param('ProtocolType',ProtocolType)

	def get_ChargeType(self):
		return self.get_query_params().get('ChargeType')

	def set_ChargeType(self,ChargeType):
		self.add_query_param('ChargeType',ChargeType)
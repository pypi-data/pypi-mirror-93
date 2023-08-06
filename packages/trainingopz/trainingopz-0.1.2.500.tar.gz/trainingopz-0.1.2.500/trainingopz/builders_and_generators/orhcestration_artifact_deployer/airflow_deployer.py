# Copyright © 2020 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import traceback

from trainingopz.builders_and_generators.orhcestration_artifact_deployer.orchestration_artifact_deployer import OrchestrationArtifactDeployer


class AirflowDeployer(OrchestrationArtifactDeployer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._path = kwargs.get('path')

    def _run(self, artifact: str):

        try:
            print("running airflow deployer... ")
            self._deploy(artifact)
        except:
            error_message = traceback.format_exc()
            self._error_handler(error_message)
            raise RuntimeError(error_message)

        return True

    def _deploy(self, artifact):
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

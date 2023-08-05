#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.lifecycle import V1Statuses
from polyaxon.polyflow.params import ParamSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class HookSchema(BaseCamelSchema):
    connection = fields.Str(allow_none=True)
    trigger = fields.Str(
        allow_none=True, validate=validate.OneOf(V1Statuses.allowable_hook_values)
    )
    hub_ref = fields.Str(required=True)
    conditions = fields.Str(allow_none=True)
    presets = RefOrObject(fields.List(fields.Str(allow_none=True)))
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(ParamSchema), allow_none=True
    )
    disable_defaults = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return V1Hook


class V1Hook(BaseConfig, polyaxon_sdk.V1Hook):
    """You can configure Polyaxon to send notifications and webhooks to users and systems
    when operations reaches a final state,
    or trigger any logic that is tightly coupled with a class of operations.

    Hooks allow you to build or set up integrations and dependencies
    based on final events generated by Polyaxon.
    External systems can subscribe or provide handling for certain events.
    When one of those events is triggered, Polyaxon will trigger the components defined
    in the hooks sections to perform a post-done logic, like sending an HTTP request
    payload to the webhook's configured URL.

    In addition to the main use-case of hooks, i.e. notifications,
    you can also use hooks to trigger a post-success logic that does
    not have to run on the same container, does not require specific accelerators,
    or is not specific to a single operation.
    For instance, you can build a custom hook to:
      * run evaluation after a training operation succeeds
      * perform data or model checks

    Polyaxon can trigger hooks when a run reaches a final status:

     * succeeded
     * failed
     * stopped
     * done (any final state)

     You can additionally provide a set of `conditions`
     to perform additional checks before triggering the logic, for instance,
     in addition to the success status, you can restrict the hook to only trigger
     if a metric has reached a certain value: `conditions: {{ loss > 0.9 }}`.

     You can resolve any context information from the main operation inside hooks,
     like params, globals, ...

     Args:
         trigger: str
         connection: str
         hub_ref: str, optional
         conditions: str, optional
         presets: List[str], optional
         disableDefaults: bool, optional
         params: Dict[str, [V1Param](/docs/core/specification/params/)], optional

    ## YAML usage

    ```yaml
    >>> hook:
    >>>   trigger: failed
    >>>   connection: slack-connection
    >>>   hubRef: slack
    ```

    ## Python usage

    ```python
    >>> from polyaxon.lifecycle import V1Statuses
    >>> from polyaxon.polyflow import V1Hook
    >>> hook = V1Hook(
    >>>     trigger=V1Statuses.FAILED,
    >>>     hub_ref="slack",
    >>>     connection="slack-connection",
    >>> )
    ```

    ## Fields

    ### connection

    The connection to notify, this [connection](/docs/setup/connections/)
    must be configured at deployment time to be used here by referencing the name.

    ```yaml
    >>> hook:
    >>>   connection: some-connection
    ```

    ### trigger

    The trigger represents the status condition to check before sending the notification.

    ```yaml
    >>> hook:
    >>>   trigger: succeeded
    ```

    In this example, the notification will be sent if the run succeeds.

    ### hubRef

    Polyaxon provides a [Component Hub](/docs/management/component-hub/)
    for hosting versioned components with an access control system to improve
    the productivity of your team.

    To trigger a hook based on a component hosted on Polyaxon Component Hub, you can use `hubRef`

    ```yaml
    >>> hook:
    >>>   hubRef: slack
    ...
    ```

    Or custom hook component

    ```yaml
    >>> hook:
    >>>   hubRef:  my-component:dev
    ...
    ```

    ### conditions

    After the main operation is done, conditions take advantage of all context values
    resolved from the main operation, including outputs, to decide if the hook can be started.


    ```yaml
    >>>   conditions: '{{ some-io-param == "some-value" }}'
    ```

    In the example above, the hook will only run if a param is passed, or an output is logged and
    is equal to "some-value".

    ### presets

    The [presets](/docs/management/ui/presets/) to use for the hook operation,
    if provided, it will override the component's presets otherwise
    the presets of the component will be used if available.

    ```yaml
    >>> operation:
    >>>   presets: [test]
    ```

    ### disableDefaults

    One major difference between hooks and normal operations,
    is that hooks will be initialized automatically with `inputs`, `outputs`, and `condition` as
    context only params, to reduce the boilerplate and the need to request usual information
    required for most notification operations.

    If you do not need these context values or if you decide to request params manually,
    you can set this field to `false`.

    ```yaml
    >>> hook:
    >>>   disableDefaults: true
    >>>   ...
    ```

    ### params

    The [params](/docs/core/specification/params/) to pass if the handler requires extra params,
    they will be validated against the inputs/outputs.
    If a parameter is passed and the component does not define a corresponding inputs/outputs,
    a validation error will be raised unless the param has the `contextOnly` flag enabled.

    ```yaml
    >>> hook:
    >>>   params:
    >>>     param1: {value: 1.1}
    >>>     param2: {value: test}
    >>>   ...
    ```
    """

    IDENTIFIER = "hook"
    SCHEMA = HookSchema
    REDUCED_ATTRIBUTES = [
        "connection",
        "trigger",
        "hubRef",
        "params",
        "conditions",
        "presets",
        "disableDefaults",
    ]

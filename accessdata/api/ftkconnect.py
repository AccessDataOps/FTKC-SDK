from .extensions import trigger_workflow_ext
from datetime import datetime, timezone

class FTKConnect():

    """
    A class that trigger the job using api call.

    :param client: The client to send the request too.
	:type client: :class: ~`accessdata.client.Client`

    """
    def __init__(self,client):
        self.client = client

    def parse_args(self,**args):

        """
        Creates workflow parameters required to be passed in api call from
        args received.

        return : workflowid and the workflow parameters 
        
        """
        workflow_details={}
        workflow_id = args["automation_id"]

        case_name_template = ""
        if 'evidence_path'in args:
            workflow_details['AddEvidence']={'EvidencePath':args['evidence_path']}
            case_name_template = case_name_template if case_name_template else "addevidence"
        if 'search_tag_path' in args:
            workflow_details['SearchAndTag']={"FolderLocation":[args['search_tag_path']]}
        if 'export_path' in args:
            workflow_details['Export']={"ExportPath":args['export_path']}

        agent_ips = []
        if 'target_ips' in args:
            agent_ips  = args['target_ips']
            if len(agent_ips)>0:
               case_name_template = agent_ips[0]
        workflow_details['Collection']={"targetips":agent_ips}

        # Process in existing case ids
        if "case_ids" in args:
            workflow_details["createCase"] = {"CaseIds":args['case_ids']}
        # Process in new case
        elif "case_ids" not in args and "case_name" in args:
            workflow_details["createCase"] = {"CaseName":args['case_name']}
        elif "case_ids" not in args and "case_name" not in args and case_name_template:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H-%M-%S")
            case_name = f"{workflow_id}_Cortex XSOAR_{case_name_template}_{timestamp}"
            workflow_details["createCase"] = {"CaseName":case_name}
        
        return workflow_id, workflow_details

    def trigger(self,**args):

        """
        Triggers the workflow api call .
        
		:return: Status of the call invoke and the response of request
		:rtype: :dict

        """
        workflow_id, workflow_params = self.parse_args(**args)
        request_type, ext = trigger_workflow_ext
        ext = ext.format(workflowid=workflow_id)
        response = self.client.send_request(request_type, ext, json=workflow_params)
        status_flag = response.json()
        result = {"Status":status_flag
                 }
        return result

import json
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_s3 as s3,
    core,
)

class PatchingStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
    
        
        #################################################
        #
        # Create maintenance windows
        # 
        #################################################

        WinMaintWindow = ssm.CfnMaintenanceWindow(self, 
                                           id='WindondsMaintwindow', 
                                           name="Windows-Maintainance-Window",
                                           cutoff=1,
                                           schedule="cron(0/30 * * * ? *)",
                                           allow_unassociated_targets=True,
                                           duration=2,
                                           description="Windows Maintainance Window"                                
                                           )     

        LinuxMaintWindow = ssm.CfnMaintenanceWindow(self, 
                                           id='LinuxMaintwindow', 
                                           name="Linux-Maintainance-Window",
                                           cutoff=1,
                                           schedule="cron(0/30 * * * ? *)",
                                           allow_unassociated_targets=True,
                                           duration=2,
                                           description="Linux Maintainance Window"
                                           )
        
        
                
        #################################################
        #
        # Create target groups
        # 
        #################################################

        
        WinMaintTarget = ssm.CfnMaintenanceWindowTarget(self,                         
                                        id='WinMaintTarget',
                                        name='Windows-Target',
                                        resource_type='INSTANCE',
                                        targets=[
                                        {
                                        "key": "tag:Patchgroup",
                                        "values": ["Windows"]}],
                                        window_id=WinMaintWindow.ref
                                        )
 
        LinuxMaintTarget = ssm.CfnMaintenanceWindowTarget(self,                    
                                        id='LinuxMaintTarget',
                                        name='Linux-Target',
                                        resource_type='INSTANCE',
                                        targets=[
                                        {
                                        "key": "tag:Patchgroup",
                                        "values": ["Linux"]}],
                                        window_id=LinuxMaintWindow.ref
                                        )
        
        
                
        #################################################
        #
        # Create tasks
        # 
        #################################################
        
        WinMaintTask = ssm.CfnMaintenanceWindowTask(self,
                                        id='WinMaintTask',
                                        name='Windows-Task',
                                        max_errors='2',
                                        max_concurrency='2',
                                        priority=1,
                                        service_role_arn="arn:aws:iam::847208056990:role/SSM-Pathcing-Role",
                                        targets=[{
                                            "key": "WindowTargetIds",
                                            "values": [WinMaintTarget.ref]
                                            }],
                                        task_type='RUN_COMMAND',
                                        task_arn='AWS-RunPatchBaseline',
                                        task_invocation_parameters={
                                                "maintenanceWindowRunCommandParameters": {
                                                    "outputS3BucketName" : "patchingsandbox",
                                                    "parameters":  {"Operation":["Scan"]}
                                            }
                                            },
                                        window_id= WinMaintWindow.ref
                                        )
        
       
        LinuxMaintTask = ssm.CfnMaintenanceWindowTask(self,
                                        id='LinuxMaintTask',
                                        name='Linux-Task',
                                        max_errors='2',
                                        max_concurrency='2',
                                        priority=1,
                                        service_role_arn="arn:aws:iam::847208056990:role/SSM-Pathcing-Role",
                                        targets=[{
                                            "key": "WindowTargetIds",
                                            "values": [LinuxMaintTarget.ref]
                                            }],
                                        task_type='RUN_COMMAND',
                                        task_arn='AWS-RunPatchBaseline',
                                        task_invocation_parameters={
                                                "maintenanceWindowRunCommandParameters": {
                                                    "outputS3BucketName" : "patchingsandbox",
                                                    "parameters":  {"Operation":["Scan"]}
                                            }
                                            },
                                        window_id= LinuxMaintWindow.ref
                                        )
        
        
        
        # Publish the custom resource output
        
        
        core.CfnOutput(
            self, "ResponseMessage02",
            description="Linux Maintenance Window ID",
            value=LinuxMaintWindow.ref
        )
        
        core.CfnOutput(
            self, "ResponseMessage03",
            description="Windows Maintenance Window ID",
            value=WinMaintWindow.ref
        )
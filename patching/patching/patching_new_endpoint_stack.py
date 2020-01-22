####################################################
#
# Create SSM endpoints and a new VPC
# Requirements: VPC with name 
# v 0.1
####################################################

import json
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_s3 as s3,
    core,
)

####################################################
#
# Variables
#
####################################################

vpcname='Sandbox'
cidr_vpc='10.10.0.0/21'
endpoint_gw = {'S3':ec2.GatewayVpcEndpointAwsService.S3 }
endpoint_if = {'E_C2_MESSAGES':ec2.InterfaceVpcEndpointAwsService.E_C2_MESSAGES, 
               'E_C2':ec2.InterfaceVpcEndpointAwsService.E_C2, 
               'SSM':ec2.InterfaceVpcEndpointAwsService.SSM,
               'SSMM':ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES}



class NewPatchingEndpointStack(core.Stack):
    

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
    
 
        #################################################
        #
        # Create new VPC
        # 
        #################################################
        
        try:
                
            
            #Subnets
            
            
            subnet_config = [
            
            {
                'cidrMask': 26,
                'name': 'ssm-public-subnet',
                'subnetType': ec2.SubnetType.PUBLIC
            },
            {
                'cidrMask': 26,
                'name': 'ssm-private-subnet',
                'subnetType': ec2.SubnetType.PRIVATE
            }]
            
            
             # Create new VPC
             
            vpc = ec2.Vpc(self, 'sandbox', 
                            cidr=cidr_vpc, 
                            enable_dns_support=True, 
                            max_azs=1,                                       
                            subnet_configuration=subnet_config
                            )
            

              
        except AssertionError as error:
            print(error)
            print('[-] Could not create VPC ' + 'SSM_VPC')
                
        
        ##################################################
        #
        # Add Security Grouup and Ingress HTTPS port (443) 
        # 
        ##################################################       
        """
        try:
                
            # Add port 443 
            #print('[+] Creating Security GRoup and adding port 443 to VPC SG: ' + vpcname)
                
            ssmSG = ec2.SecurityGroup(self, "SSM Security Group",
                                            vpc=vpc,
                                            allow_all_outbound=True,
                                            security_group_name="ssm_sg " + vpcname
                                                  
                                            )
            
    
            # Add 443 port ingress rule
            
            ssmSG.add_ingress_rule(peer=ssmSG, connection=ec2.Port.tcp(443))           
 
        except AssertionError as error:
            print(error)
            print('[-] Could not find Security Group')
        
        """
        ##################################################
        #
        # Create new VPC Endpiont Gateway(s)
        # 
        ##################################################       
        
        for endpoint in endpoint_gw:

            try:
                
                #print('[+] Setting up GW Endpoint ' + str(endpoint))
                
                s3_endpoint = vpc.add_gateway_endpoint(endpoint, service=endpoint_gw[endpoint])
                
            except AssertionError as error:
                print(error)
                print('[-] Error creating Gateway Endpoint')
 
 
        ##################################################
        #
        # Create new VPC Endpoint Interface(s)
        # 
        ##################################################  

        
        for endpoint in endpoint_if:
            
            #print('[+] Endpoint: ' + str(endpoint))
            
            try:
                
                #print('[+] Setting up Interface Endpoint: ' + str(endpoint))
                
                if_endpoint = vpc.add_interface_endpoint(endpoint, service=endpoint_if[endpoint])
                
                # Add SG
                if_endpoint.connections.allow_default_port_from_any_ipv4()
                
            except AssertionError as error:
                print(error)
                print('[-] Error creating Interface Endpoint')

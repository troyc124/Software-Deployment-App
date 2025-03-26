import os
import time
import uuid
import socket
import platform
import requests
import threading

class DeploymentClient:
    def __init__(self, server_url, api_token):
        self.server_url = server_url
        self.api_token = api_token
        self.client_id = str(uuid.uuid4())
        self.hostname = socket.gethostname()
        self.os_type = platform.system().lower()

    def register_client(self):
        """Register the client with the deployment server"""
        try:
            response = requests.post(
                f"{self.server_url}/api/clients/register/", 
                json={
                    'hostname': self.hostname,
                    'os_type': self.os_type,
                    'client_id': self.client_id
                },
                headers={'Authorization': f'Token {self.api_token}'}
            )
            return response.status_code == 201
        except requests.exceptions.RequestException as e:
            print(f"Registration failed: {e}")
            return False

    def check_in(self):
        """Periodically check in with the server to update status"""
        while True:
            try:
                requests.post(
                    f"{self.server_url}/api/clients/checkin/",
                    json={'hostname': self.hostname},
                    headers={'Authorization': f'Token {self.api_token}'}
                )
            except requests.exceptions.RequestException:
                pass
            time.sleep(300)  # Check in every 5 minutes

    def poll_deployments(self):
        """Poll for pending deployments"""
        while True:
            try:
                response = requests.get(
                    f"{self.server_url}/api/deployments/pending/",
                    params={'hostname': self.hostname},
                    headers={'Authorization': f'Token {self.api_token}'}
                )
                
                if response.status_code == 200:
                    deployments = response.json()
                    for deployment in deployments:
                        self.process_deployment(deployment)
            
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(60)  # Poll every minute

    def process_deployment(self, deployment):
        """Simulate software deployment"""
        try:
            # Simulate installation process
            print(f"Processing deployment: {deployment['package_name']}")
            time.sleep(10)  # Simulate installation time
            
            # Report deployment status
            requests.post(
                f"{self.server_url}/api/deployments/update/",
                json={
                    'deployment_id': deployment['id'],
                    'status': 'completed'
                },
                headers={'Authorization': f'Token {self.api_token}'}
            )
        except Exception as e:
            print(f"Deployment failed: {e}")

    def start(self):
        """Start client services"""
        if not self.register_client():
            print("Failed to register client. Exiting.")
            return

        # Start background threads
        checkin_thread = threading.Thread(target=self.check_in, daemon=True)
        deployment_thread = threading.Thread(target=self.poll_deployments, daemon=True)
        
        checkin_thread.start()
        deployment_thread.start()

        # Keep main thread running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Client stopping...")

if __name__ == "__main__":
    SERVER_URL = "http://localhost:8000"
    API_TOKEN = "your_api_token_here"
    
    client = DeploymentClient(SERVER_URL, API_TOKEN)
    client.start()
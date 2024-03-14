import os
from fastapi import APIRouter, HTTPException
import boto3

COGNITO_REGION = os.getenv("COGNITO_REGION")
COGNITO_POOL_ID = os.getenv("COGNITO_POOL_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CHALLENGE_NAME = os.getenv("CUSTOM_CHALLENGE")
ANSWER = "ANSWER=opensesame,USERNAME="
AUTH_FLOW = os.getenv("AUTH_FLOW")
client = boto3.client("cognito-idp", region_name=COGNITO_REGION)
router = APIRouter()

@router.post("/signup")
def signup(username: str, password: str):
    try:
        client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=password,
        )
        return {"message": "User signed up successfully"}
    except client.exceptions.UsernameExistsException:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-token")
def generate_token(username: str = None):
    try:
        session = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow=AUTH_FLOW,
            AuthParameters={'USERNAME': username}
        )
        
        session = session['Session']
        token = client.respond_to_auth_challenge(
            ClientId=CLIENT_ID,
            Session=session,
            ChallengeName=CHALLENGE_NAME,
            ChallengeResponses=parse_challenge_responses(ANSWER + username)
        )['AuthenticationResult']['AccessToken']
        
        return token

    except Exception:
        raise HTTPException(status_code=404, detail="Usuário não autenticado!")
    
def parse_challenge_responses(challenge_responses: str):
    parsed_responses = {}
    for response in challenge_responses.split(","):
        key, value = response.split("=")
        parsed_responses[key] = value
    return parsed_responses
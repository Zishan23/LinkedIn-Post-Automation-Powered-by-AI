import os
import requests
import logging
from config.development import get_headers

# LinkedIn API endpoints
POST_URL = "https://api.linkedin.com/v2/ugcPosts"
ASSETS_REGISTER_UPLOAD_URL = "https://api.linkedin.com/v2/assets?action=registerUpload"

# Get PERSON_URN_KEY from environment - use correct format that LinkedIn expects
PERSON_URN_KEY = os.getenv('PERSON_URN_KEY', 'urn:li:person:zEDX9e-ab3')

def upload_image(image_path):
    """Upload image to LinkedIn following Microsoft Learn documentation exactly"""
    try:
        HEADERS = get_headers()
        
        # Add the REQUIRED header from Microsoft Learn documentation
        HEADERS["X-Restli-Protocol-Version"] = "2.0.0"
        
        # Follow exact structure from documentation
        data = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": PERSON_URN_KEY,
                "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}],
            }
        }
        
        logging.info(f"Registering image upload with data: {data}")
        
        res_data = requests.post(ASSETS_REGISTER_UPLOAD_URL, json=data, headers=HEADERS)
        
        if res_data.status_code != 200:
            logging.error(f"Image registration failed: {res_data.status_code} - {res_data.text}")
            raise Exception(f"Image registration failed: {res_data.status_code}")
            
        res_json = res_data.json()
        logging.info(f"Image registration successful: {res_json}")
        
        if "value" not in res_json:
            logging.error(f"Unexpected response format: {res_json}")
            raise Exception(f"Unexpected response format: {res_json}")
            
        upload_url = res_json["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        image_asset = res_json["value"]["asset"]
        
        # Upload the actual image file
        with open(image_path, "rb") as image_file:
            upload_response = requests.post(upload_url, data=image_file.read(), headers=HEADERS)
            
            if upload_response.status_code not in [200, 201]:
                logging.error(f"Image file upload failed: {upload_response.status_code} - {upload_response.text}")
                raise Exception(f"Image file upload failed: {upload_response.status_code}")
                
            logging.info(f"Image file upload successful: {upload_response.status_code}")
            return image_asset
            
    except Exception as e:
        logging.error(f"Error in upload_image: {e}")
        raise e

def post_to_linkedin(content, image_path):
    """Post content to LinkedIn following Microsoft Learn documentation exactly"""
    try:
        HEADERS = get_headers(content_type="application/json")
        
        # Add the REQUIRED header from Microsoft Learn documentation
        HEADERS["X-Restli-Protocol-Version"] = "2.0.0"
        
        # Try to upload image first
        image_asset = None
        try:
            image_asset = upload_image(image_path)
            logging.info(f"Image uploaded successfully: {image_asset}")
        except Exception as e:
            logging.warning(f"Image upload failed, will post text only: {e}")
        
        # Follow exact structure from Microsoft Learn documentation
        if image_asset:
            # Create image post following documentation exactly
            post_data = {
                "author": PERSON_URN_KEY,  # Required field - Person URN
                "lifecycleState": "PUBLISHED",  # Required field
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": content},
                        "shareMediaCategory": "IMAGE",
                        "media": [{
                            "status": "READY",
                            "description": {"text": content},
                            "media": image_asset,
                            "title": {"text": "LinkedIn Post"}
                        }],
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            }
        else:
            # Create text-only post following documentation exactly
            post_data = {
                "author": PERSON_URN_KEY,  # Required field - Person URN
                "lifecycleState": "PUBLISHED",  # Required field
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": content},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            }
        
        logging.info(f"Attempting LinkedIn post with data: {post_data}")
        logging.info(f"Headers: {HEADERS}")
        
        response = requests.post(POST_URL, json=post_data, headers=HEADERS)
        
        if response.status_code in [200, 201]:
            logging.info(f"✅ SUCCESS! LinkedIn post successful: {response.status_code}")
            return {"success": True, "message": "Post created successfully", "response": response.json()}
        else:
            logging.error(f"LinkedIn posting failed: {response.status_code} - {response.text}")
            raise Exception(f"LinkedIn posting failed: {response.status_code} - {response.text}")
        
    except Exception as e:
        logging.error(f"Error in post_to_linkedin: {e}")
        return {"success": False, "error": str(e)}

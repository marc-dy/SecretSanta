# Pre-requisite
1. Python should be instealled in your computer
2. Setup access to GMail's SMTP Server
   1. Enable 2-step verification in your Gmail account settings
   2. Generate an app password for your Python script
   3. Generated app password will be added to the sender_password in your json file.

# How to use:
1. Create a json file based on the template.json in the same path as SecretSanta.py
2. (Optional) Add images using the name of the person in .jpg format
   - Example:
      - In json file:
         - "name": "Juan"
      - Image name should be Juan.jpg
3. Run `python ./SecretSanta.py`
4. Enter json file name when asked by the script

# Limitations:
1. Currently assumes sender email is using a gmail account

   

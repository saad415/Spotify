import pandas as pd

def get_user_profile(sp):
   
    user_profile = sp.current_user()
    # Extract the required information
    profile_picture = user_profile['images'][0]['url'] if user_profile['images'] else None
    display_name = user_profile['display_name']
    email = user_profile['email']
    country = user_profile['country']

    # Create a DataFrame with the user information  
    user_data = pd.DataFrame({
    "Profile Picture": [profile_picture],
    "Display Name": [display_name],
    "Email": [email],
    "Country": [country]
    })

    return user_data


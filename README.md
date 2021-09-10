<p align="center">
  <h1 align="center">⚙️ gtm-gear</h1>

  <p align="center">    
    Automate everyday Google Tag Manager tasks.
    <br />
  </p>
</p>

<!-- ABOUT THE PROJECT -->

## About The Project
If you have a bunch of sites with the same or similar Google Tag Manager setup, and your daily job is to keep all containers in consistent state - make all needed changes only in one container, tests everything and then use ⚙️ gtm-gear to sync changes between containers.

Or if you have base set up for GA/GAds/DV360/Facebook/... you can once save it and then push to new client's GTM container with a few lines of code 💪.

_Project is still in work the current version is 0.1_

 **Main scenarios 🔥:** 
- Get tags, triggers, variables, built in variables, folders by API;
- Cache all data to reduce amount of requests;
- Limit request rate to 25 by 100 seconds as its default limit for GTM API;
- Update params you need;
- Set tags on pause;
- Create new workspaces;
- Copy tags between containers;
- Copy everything in version to other container;
- Check the difference between containers;
- Clean container: delete tags on pause, delete not used variables and triggers.


### Built With

- [Python](https://www.python.org/)
- [GTM API](https://developers.google.com/tag-manager/api/v2)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.  

1. ### Init virtual environment
   ```sh
   virtualenv --python=python3.8 .venv
   ```
2. ### Enter in

   ```sh
   source .venv/bin/activate

   ```

3. ### Install requirements

   ```sh
   python -m pip install -r requirements.txt
   ```

3. ### Get credentials for GTM API

   
   Follow steps from the [documentation](https://developers.google.com/tag-manager/api/v2/authorization)
   

4. ### Set path to credentials

   
   Set path to folder with `client_secrets.json` and `tagmanager.dat`.

   In code: 
   ```os.environ["GTM_API_CONFIG_FOLDER"] = 'path'```
   


<!-- USAGE EXAMPLES -->

## Usage

_For examples, please refer to the samples folder_

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

Artem Korneev - [linkedin](https://www.linkedin.com/in/artem-korneev-99509137/)

# discord-bot-template
To serve as a template for a discord bot that runs as a docker container with MongoDB as a database

# Disclaimers
- This isn't some end-all-be-all solution, it's what I managed to design as a template for the discord bot I've developed
- This is designed to be very generic so that it can run in multiple servers
- Every command has to have permissions configured for, unless the user has the `Administrator` permission.
- Validated for only `Python 3.11`

## Docker
This is designed to run the database, DB web interface, and the bot within docker containers, so make sure to have that installed and configured.

## MongoDB
- Why MongoDB?
  - Because I found it very easy to work with and I don't expect hundreds of thousands of records to be created
- Why a database?
  - Do you really want to code out all the log for inserts, updates, removes, etc.?
- What is `overwrite/router.js` for?
  - There's currently a bug with `mongo-express` where you're not able to view the database statistics, this fixes that.

# Setting up the bot
You don't need this running inside a docker container. As you're developing the bot you can run it locally and just have the database and database web interface running
## Virtual Environment
It's best to set yourself up with a virtual environment

- First make sure you have `Python 3.11` installed
- In the project run, `python -m venv discord-bot`
- Add `discord-bot/*` to the `.dockerignore` and `.gitignore` files
- Activate your environment
  - You can find the acivate scripts under `./discord-bot/Scripts`
- Install the required packages via `pip install -r requirements.txt`

## Environment Variables
Make sure to rename `.sample.env` to `.env` and update the values with appropriate values

## Docker Containers

### Building the Containers
Run `docker-compose up -d`
<br><br>

### Stopping the Contaiiners
Run `docker-compose stop`
<br><br>

### Destroying the Contaiiners
Run `docker-compose down`

# Command Examples
**If there are double quotes around something, that means it's required**
- Allowing users to run the `hug` command
  - `!permissions set "hug" add users "123, 456"`
  - `!p s "hug" a u "123, 456"`
- Removing users from being able to run the `hug` command
  - `!permissions set "hug" remove users "123, 456"`
  - `!p s "hug" rm u "123, 456"`
- Allowing roles to run the `hug` command
  - `!permissions set "hug" add roles "123, Admin"`
  - `!p s "hug" a r "123, 456"`
- Removing users from being able to run the `hug` command
  - `!permissions set "hug" remove roles "123, Admin"`
  - `!p s "hug" rm r "123, 456"`
- Prining out the permissions for the `hug` command
  - `!permissions get "hug"`
  - `!p g "hug"`
- Resetting the permissions for the `hug` command
  - `!permissions reset "hug"`
  - `!p rst "hug"`
- Reloading the cogs
  - `!reload`
  - `!r"`

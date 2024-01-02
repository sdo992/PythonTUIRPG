# Python TUI-based RPG
#### Code license:
<p align="left">
  <a aria-label="Code license" href="https://github.com/primer/css/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/primer/css.svg" alt="">
  </a>
</p>

#### Written content license:

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Goals
------------------
- AI-based NPC control/interaction; need to find training material; I have a couple databases, will need to contact an attorney to make sure it's legally acceptable in my area
- [notcurses](https://github.com/dankamongmen/notcurses) game client
- Living, breathing world controlled by different AIs; these will need to be as lightweight as possible and yet fulfill their function
  - Weather AI, based on geography
  - NPC AI
    - Monsters/combatants
    - Quest
    - Socio-political
- Create an *interesting and enjoyable game* rather than focus on the latest, most beautiful graphics possible
- Sandbox-type world

Current Development Status
------------------
These files are the 2nd or 3rd iteration of my attempts to successfully create a login client/server and world server in python.

Python3-based TUI RPG. Currently, this consists of:
- Login client: Using curses
- Login server: The backend is sqlite; passwords are hashed between client and server
- World server: This does nothing at the moment except to provide a message that the user connection is successful. Eventually, will control a notcurses-based client

Roadmap
------------------
This project is in pre-alpha as of 01 January 2024. I am working on the goals and logic flow, which I may post here later which will guide technology development.

- Hardware requirements
  - [x] Dedicated world server; already own 2x AMD systems that will work through alpha stage; will keep an eye out for older commercial-grade server hardware
  - [x] Dedicated login server; ideally, I would like something simple and lightweight, such as a Raspberry Pi - `Need to evaluate effectiveness and capabilities/stress test`
- Enter alpha stage on `login_client.py`
  - [ ] Create own instance of terminal window upon launching the client
  - [ ] Port code to notcurses to allow for custom graphics (*Nice to have*)
  - [ ] Center username and password on terminal window
    - [ ] Message to create account on website or by someother means if one does not exist
    - [ ] Error message popup if account does not exist
  - [ ] Close gracefully after passing user off to game client
- Enter alpha stage on `login_server.py`
  - [ ] Encrypt communication between login client and login server
    - [x] password hash
    - [ ] username hashed between client/server
  - [ ] Encrypt communication between login server and world server
- Enter alpha stage on `world_server.py`
  - [ ] Check if account is active
    - [ ] If account is active, successfully route user to game world
    - [ ] If account is inactive, reroute to login client with error message
  - [ ] Notify login client that user login was successful to close login client
  - [ ] Server-side exception handling and log errors to file
  - [ ] Notify admin on server exception
  - Admin-specific functions
    - [ ] Start
    - [ ] Stop
    - [ ] Reboot
    - [ ] Status query
  - User functions, `to be identified at a later date`
- Create NPC database
- Create AI-based NPC interaction
  -  [ ] AI learning model for YAML/JSON files

Notes
------------------
Almost all of the goals and development is subject to change; however, what I'm absolutely tied to is that I want this done with SQLite and Python. I may port this later on, but I want to test scalability and effectiveness in resource handling.

Concept, art and code written by **[Steven Osborne](mailto:fjallravn@runbox.com)**

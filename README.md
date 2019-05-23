# Social Abstraction

Setting up a reverse proxy from public DNS can be cumbersome. Using Docker and Bash, here is an approach that creates the endpoint `sa.jbcurtin.io`, creates an SSH tunnel and links a facebook app your local development enviornment

## Features

- Completely encapsulated opertaion that'll setup a reverse proxy
- Completely encapsulated operation that'll create a database to connect to on localhost using docker
- Allows user to Login
- (incomplete) Sets user to inactive if user removes facebook app


## Setup Reverse Proxy

- Launch an EC2 instance
- Update all DNS A records HOST_NAME.domain.tld
- Create an SSH configuration entry for seemless access
- run bootstrap script `$ bash operations.sh bootstrap`

TODO ::
Create modular sections. for installing node.

### Setup Git Commit Messaging Lint

Tools Used :

- [Git](https://github.com)
- [node](https://nodejs.org/en/)
- [Commitzen](http://commitizen.github.io/cz-cli/#making-your-repo-commitizen-friendly)

Note: Following steps are intended to install node modules locally so that all the devs would be using the same version of commitzen and other tools.

Assumes that you had

- initiated git in the project
- Installed node globally or at local level or provided with some node virtual environment tools like [nodeenv](https://github.com/ekalinin/nodeenv)

If project is not based on node(eg. is a python project or some other language project). Initialize the node package management in the project directory by following commands

else, skip to step 2 as most likely, As its node based you would have already initiated the project with node.

```bash

# Step 1
# Sets up project with ability to utilize node packages.
npm init -y

```

```bash

# Step 2
# Install commitzen
npm install --save-dev commitizen

# Step 3
# Make project commitzen friendly
# In sense sort of, Sets up command line to prompt during git commit
npx commitizen init cz-conventional-changelog --save-dev --save-exact

```

Step 4 :

Now in the file .git/hooks/prepare-commit-msg
add following lines.

```bash
#!/bin/bash
exec < /dev/tty && node_modules/.bin/git-cz --hook || true
```

```bash
# Sanitize
rm -rf env/ node_modules/ package.json package-lock.json commitlint.config.js commitlint.config.jsnpm

nodeenv env

. env/bin/activate
```

if you did not setup the node.
Install and initiate in your project

```bash
# Initiating node
npm init -y
```

### Setting up Commitlint

```bash
# install commitlint
npm install --save-dev @commitlint/cli
```

### Setting up Husky

```bash
# Install Husky
npm install --save-dev husky
```

```json
// append or modify following fields in package.json

  "husky": {
    "hooks": {
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS"
    }
   }
```

### Set up Prompt

As its hard to remember all the topics. Provide options to select from, instead to write the repetitive labels manually.

```bash
# install commitizen
npm install --save-dev commitizen

# install commitiquette
# Used to make commitizen use commitlint
# configurations.
npm install commitiquette --save-dev

```

Modify or append following fields in package.json to link commitzen prompt with commitlint prompts. One may directly use commit lint prompt with 'npm run commit' without commitzen. But commitzen provides,
prompt directly when run 'git commit' command. This is inlines with workflow much better. Note Commitzen here triggers to use commit lint prompt again.

```json
# Modify or append following fields in package.json

  "config": {
    "commitizen": {
      "path": "commitiquette"
    }
  }

```

### Set up Lint Configuration

Adapters or Configuration for linting.
[Available Configurations](https://github.com/conventional-changelog/commitlint#shared-configuration)

Using ~~Angular Commit Conventions~~ config-conventional

```bash
# install Angular Commit Conventions for commit lint
npm install --save-dev @commitlint/config-conventional
# setup the commit lint config files with installed configurations
echo "module.exports = {extends: ['@commitlint/config-conventional']};" > commitlint.config.js
```

Add support for Travis CI Checks

```bash
# Install and configure if needed
npm install --save-dev @commitlint/travis-cli
```

Configure Travis CI setup

```yml
# travis.yml
language: node_js
node_js:
  - node
script:
  - commitlint-travis
```

hint : For multiple languages try travis matrix.
Something like this.

```yml
# travis.yml
matrix:
  include:
    - language: node_js
      node_js:
        - node
      script:
        - npm install --save-dev
        - commitlint-travis

    # Using Python : To build the Docker and run Django app.
    - language: python
      # The python version that we need to use.
      # it has to be available in travis channel
      # but we are using docker's python no need to worry about this.
      python:
        - "3.8"
      # telling travis CI what services we are going to use
      services:
        - docker
      # A script that travis runs before it executes any of automation commands defined later here.
      # We need docker-compose
      before_script: pip install docker-compose
      # Running the script for tests and linting
      script:
        - docker-compose run app sh -c "python manage.py test && flake8"
      # when ever a change in git is detected.
      # So spins a travis python server of version 3.8
      # makes service docker available.
      # runs a before script. i.e. to install docker compose
      # then runs the script i.e performs tests and checks for linting.
```

To avoid merging unsuccessful builds,
In git hub repository
-> settings
-> branches
-> Check Require Status Checks to pass before running
-> Require branches to be up to date before merging
-> Check Travis CI - Branch

Further Improvement ::

- You can set [scope prompts and rules](https://commitlint.js.org/#/reference-rules). eg.

```yml
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "scope-enum": [2, "always", ["core", "lib", "misc", "etc", "ci cd tools"]],
  },
};
```

- During the time of writing these packages were just started and has huge potential for improvements.
  Check back if can upgrade the workflow.

  - [Customize Commitizen](https://github.com/leonardoanalista/cz-customizable)
  - [devmoji](https://github.com/folke/devmoji)

## Semantic Release Setup:

Following configuration is to setup project irrespective of language used.
A good tutorial can be found in this [link](https://hodgkins.io/automating-semantic-versioning#Installation)

### Sanitize

Execute only when you want to test semantic release removing all other installed stuff

```bash
# Sanitizing.
# Pay attention :::::: This will remove all the files

rm -rf env/ node_modules/ package.json package-lock.json .releaserc .github/workflows/release.yml

nodeenv env

. env/bin/activate
```

if you did not setup the node.
Install and initiate in your project

```bash
# Initiating node
npm init -y
```

```bash
# Install semantic-release
npm install --save-dev semantic-release               \
    @semantic-release/changelog               \
    @semantic-release/commit-analyzer         \
    @semantic-release/exec                    \
    @semantic-release/git                     \
    @semantic-release/release-notes-generator
```

Create a `.releaserc` File with following configuration

```
{
  "branch": "master",
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    [
      "@semantic-release/npm",
      {
        "npmPublish": false
      }
    ],
    [
      "@semantic-release/changelog",
      {
        "changelogFile": "CHANGELOG.md",
        "changelogTitle": "# Semantic Versioning Changelog"
      }
    ],
    [
      "@semantic-release/git",
      {
        "assets": [
          "CHANGELOG.md"
        ]
      }
    ],
    [
      "@semantic-release/github",
      {
        "assets": [
          {
            "path": "dist/**"
          }
        ]
      }
    ]
  ]
}
```

### Create a github token

-> go to Github.com

-> Top Right Corner

-> Settings

-> Developer Settings

-> Personal Access Tokens

-> generate

Note : Check the following scopes for the token

- [ ] repo:status
- [ ] repo_deployment
- [ ] public_repo

Note :: Copy and store it for a while as we need it in configuring github secrets later.

for testing it locally

```bash
export GITHUB_TOKEN=PUT-YOUR-TOKEN-HERE
```

Run the following command to invoke semantic release
change log generation

```bash
npx semantic-release

# You can also run it with the --debug flag for more details.
```

### Configuring the Git hub Secrets

Goto

-> github.com

-> go to your repo

-> go to the repo settings not the top right corner settings

-> left bar : secrets

-> new secret

Try using name as `SEMANTIC_RELEASE_SECRET` Or as required. Copy the personal token you generated in above section creating a github token.

### Configuring Git Actions for semantic release.

A good source instructions can be found in this [link](https://github.com/semantic-release/semantic-release/blob/master/docs/recipes/github-actions.md)

Configure the git actions in `.github/workflows/release.yml`

Note:

- For GITHUB_TOKEN use the secret name you had configured if you did not named it `SEMANTIC_RELEASE_SECRET`

- We are not using any npm publishing. if thats the intent, its not covered here. you need to check the official [semantic release site](https://semantic-release.gitbook.io/semantic-release/) the tutorial there is pretty straight forward to do so. You must specify this line in semantic release configuration file
  `[ "@semantic-release/npm", { "npmPublish": false } ],`
  else it shows error either prepare.sh not found etc.
  If you are using npm toggle back accordingly.
- In future if you intend to do some advanced stuff try [this git hub actions published](https://github.com/marketplace/actions/action-for-semantic-release).
- kind of same as above but got some output features [link](https://github.com/marketplace/actions/semantic-release-action#outputs)

```yml
# .github/workflows/release.yml
name: Release
on:
  push:
    branches:
      - master
jobs:
  release:
    name: Release
    runs-on: ubuntu-18.04
    steps:
      - name: Checkout
        uses: actions/checkout@v1
      - name: Setup Node.js
        uses: actions/setup-node@v1
        with:
          node-version: 12
      - name: Install dependencies
        run: npm ci
      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.SEMANTIC_RELEASE_SECRET }}
        run: npx semantic-release
```

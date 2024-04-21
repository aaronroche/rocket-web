
# Welcome to your CDK Python project!

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`ec2_cdk_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


## Required Modifications to Run Project
This project requires the user to have an `AWS access key ID`, `secret access key`, and an existing key pair.

First, find the file `.env`. Then, substitute with your `AWS access key ID` and a `secret access key`.

Next, find the file `EC2Stack.py` located in the folder `ec2_stack`. Now, find this line of code `key_pair = ec2.KeyPair.from_key_pair_name(self, "KeyPair", "RonKeyPair")`. Change `RonKeyPair` to the name of your existing keypair.

Now, run these commands to allow your computer to run these bash scripts.
`chmod +x event_bridge.sh`
`chmod +x deploy_and_run`

Run the project using the command and bash scripts using `./deploy_and_run.sh` in your terminal.

That's everything. Enjoy!

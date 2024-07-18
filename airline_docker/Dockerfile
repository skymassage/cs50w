# We may have a different version of some additional packages installed 
# that allow the app to run smoothly on our computer, while it would crash on our server.
# To avoid these problems, we need a way to make sure everyone working on a project is using the same environment.
# One way to do this is to use a tool called Docker, which is a containerization software, 
# meaning it creates an isolated environment within your computer that can be standardized among many collaborators 
# and the server on which your site is run.
# While Docker is a bit like a Virtual Machine, they are in fact different technologies. 
# A virtual machine is effectively an entire virtual computer with its own operating system, 
# meaning it ends up taking a lot of space wherever it is running. 
# Dockers, on the other hand, work by setting up a container within an existing computer, therefore taking up less space.

# First, create a Docker File which we typically name "Dockerfile", 
# because Docker will by default search for a file named Dockerfile in the directory. 
# Inside of Dockerfile, we'll provide instructions for how to create a Docker Image which describes the libraries 
# and binaries we wish to include in our container.

FROM python:3
COPY .  /usr/src/app
WORKDIR /usr/src/app
# We can also set the current working directory before copying the files to the container.
# The following is the same as abve:
# WORKDIR /usr/src/app
# COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


# FROM <image_name>:<tag>: Construct our image based on the <image_name>:<tag Image>.
#                          We don't want to create a Docker image from setting up the environment, so most of the time, 
#                          we will directly find the Image that has already set up the environment from DockerHub as a base to create our own Image.
#                          "From" first searches for the matching image from the local Docker image,
#                          and if it cannot find it, it will download it from DockerHub.
#                          Here we use "Python:3" as the base Image to build our own Image.
# COPY <directory_1> <directory_2>: Copy everything (except Dockerfile) from the directory <directory_1>
#                                   and store it n the new container's directory <directory_2>.
# WORKDIR <directory>: WORKDIR means to change the working directory to <directory>. (A bit like the "cd" command on the terminal)
#                      So this sets up where we will run commands within the container. 
#                      Here we would like to set our working directory equal to that same app directory, 
#                      the app directory inside of the container that now contains all of the files from my app
#                      because I copied all of those files into the container. 
# RUN pip install -r requirements.txt: "RUN" means to execute Shell command.
#                                      Assuming we've included all of your requirements (like Django and any other packages) 
#                                      to a file called "requirements.txt", they will all be installed within the container.
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]: Specify the command that should be run when we start up the container.

# CMD ["command_name", "argv1", "argv2", ...]: CMD means to the first command to be executed when the container is started up.
#                                              Here, when the container starts, the "python3 manage.py runserver" shell script will be executed first.
#                                              Beside, we just specify on what address and what port we would like it to run. 
#                                              And we run it on port 8000, for example. But we could choose another port that we would like to run instead.

# RUN will be executed when the image is created.
# And CMD won't be executed when the image is created, but the container is started based on the image.
# CMD should be always the last instruction line in the Dockerfile.
"""Main script"""
import config.conf as config
from logger.logger import Logger
from modules.ssh_client import SSHClient
from modules.ec2_manager import Instance

list_of_instances = "instances_list"

if __name__ == "__main__":
    logger_instance = Logger()
    logger = logger_instance.logger
    ssh_client = SSHClient(logger)
    # Read list of instances
    with open(list_of_instances) as file:
        instances_list = file.read().splitlines()
    for instance_type in instances_list:
        logger.info(f"Trying to start: {instance_type}")
        try:
            # start instance
            instance = Instance(logger, instance_type)
            instance_ip = instance.instance_ip()
            # execute command on the instance
            command = "uname -a"
            result = ssh_client.execute_ssh_command(config.instance_user,
                                                    command,
                                                    instance_ip,
                                                    config.private_key_path)
            if result == 0:
                logger.info(f"Successfully started: {instance_type}")
        except Exception:
            logger.error(f"Failed boot: {instance_type}")
        try:
            # terminate instance
            instance.terminate()
            logger.info('Successfully terminated.')
        except Exception:
            logger.error("Can't terminate")

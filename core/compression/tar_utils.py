import tarfile
import os
import logging

def compress_backup(backup_file: str, output_file: str, logger: logging.Logger) -> None:
    """
    Compress a backup file into a tar.gz archive.

    :param backup_file: The path to the backup file to compress
    :param output_file: The path where the compressed file will be saved
    :param logger: Logger instance for logging compression operations
    """
    try:
        # Check if the backup file exists before attempting to compress
        if not os.path.isfile(backup_file):
            logger.error(f"Backup file '{backup_file}' does not exist.")
            raise FileNotFoundError(f"Backup file '{backup_file}' does not exist.")
        
        with tarfile.open(output_file, "w:gz") as tar:
            tar.add(backup_file, arcname=os.path.basename(backup_file))
        
        logger.info(f"Backup compressed successfully to '{output_file}'.")

    except tarfile.TarError as e:
        logger.error(f"Error while compressing backup file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during compression: {e}")
        raise

def decompress_backup(compressed_file: str, logger: logging.Logger) -> str:
    """
    Decompress a tar.gz backup archive.

    :param compressed_file: The path to the compressed file
    :param logger: Logger instance
    :return: Path to the decompressed file
    """
    try:
        if not os.path.isfile(compressed_file):
            logger.error(f"Compressed file '{compressed_file}' does not exist.")
            raise FileNotFoundError(f"Compressed file '{compressed_file}' does not exist.")
        
        extract_path = os.path.dirname(compressed_file)
        with tarfile.open(compressed_file, "r:gz") as tar:
            # We assume one file per archive for now as per our compress_backup implementation
            member = tar.next()
            if member:
                tar.extract(member, path=extract_path)
                decompressed_file = os.path.join(extract_path, member.name)
                logger.info(f"Backup decompressed successfully to '{decompressed_file}'.")
                return decompressed_file
            else:
                raise Exception("Archive is empty.")

    except Exception as e:
        logger.error(f"Error while decompressing backup file: {e}")
        raise

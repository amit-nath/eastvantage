from sqlalchemy.orm import Session

from address_book import logger, models, schemas


def get_address_by_id(db: Session, address_id: int):
    logger.debug(
        f'Fetching address from database using address_id: {address_id}')
    address = db.query(models.Address).filter(
        models.Address.id == address_id).first()
    logger.debug(f'Found address with id {address_id} - {address}')
    return address


def get_address_by_latitude_and_longitude(db: Session, latitude: str, longitude: str):
    logger.debug(
        f'Fetching address from database using latitude - {latitude} and longitude - {longitude}')
    address = db.query(models.Address).filter(
        models.Address.latitude == latitude, models.Address.longitude == longitude).first()
    logger.debug(
        f'Found address {address} with latitude - {latitude} and longitude - {longitude}')
    return address


def get_addresses(db: Session, skip: int = 0, limit: int = 20):
    logger.debug(
        f'Fetching addresses from database using offset - {skip} and limit - {limit}')
    addresses = db.query(models.Address).offset(skip).limit(limit).all()
    logger.debug(f'Addresses stored in database are - {addresses}')
    return addresses


def create_address(db: Session, address: schemas.AddressCreate):
    logger.debug(f'Creating new address with - {address}')
    db_address = models.Address(
        latitude=address.latitude, longitude=address.longitude)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    logger.debug(f'Successfully created new address')
    return db_address


def delete_address(db: Session, address: schemas.AddressDelete):
    logger.debug(
        f'Deleting address with latitude - {latitude} and longitude - {longitude}')
    db_address = db.query(models.Address).filter(
        models.Address.latitude == latitude, models.Address.longitude == longitude).first()
    db_address.delete()
    db.commit()
    logger.debug(f'Successfully deleted address from database')


def delete_address_by_id(db: Session, address_id: int):
    logger.debug(f'Deleting address with id - {address_id}')
    db_address = db.query(models.Address).filter(
        models.Address.id == address_id).first()
    print('-'*80)
    print(db_address)
    db.delete(db_address)
    db.commit()
    logger.debug(f'Successfully deleted address from database')

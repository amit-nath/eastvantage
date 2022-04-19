from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from address_book import crud, logger, models, schemas
from address_book.database import SessionLocal, engine
from address_book.utils import get_distance

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
logger.debug('FastAPI app initiated')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
        logger.debug('Database connection initiated')
    finally:
        db.close()
        logger.debug('Database connection closed')


@app.post("/addresses/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    try:
        logger.debug(
            f'Recieved address create request with - {address}')
        db_address = crud.get_address_by_latitude_and_longitude(
            db, latitude=address.latitude, longitude=address.longitude)
        if db_address:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Address already exists")
    except Exception as e:
        logger.error(
            f'Failed to create address - {address}', exc_info=True)
    return crud.create_address(db=db, address=address)


@app.get("/addresses/", response_model=list[schemas.Address])
def read_addresses(latitude: int = 0, longitude: int = 0 , distance: int = 0, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    try:
        logger.debug(
            f'Recieved read request for all addresses with offset {skip} and limit {limit}')
        addresses = crud.get_addresses(db, skip=skip, limit=limit)
        logger.debug(f'Addresses found are - {addresses}')
        logger.debug(f'distance - {distance}')
        logger.debug(f'distance - {float(distance)}')
        if float(distance):
            temp = []
            for address in addresses:
                if get_distance(float(latitude), float(address.latitude), float(longitude), float(address.longitude)) > float(distance):
                    temp.append(address)
                else:
                    logger.debug(f'Distance between {float(latitude)}, {float(longitude)} and {float(address.latitude)}, {float(address.longitude)} is > {distance}')
            addresses = temp
    except Exception as e:
        logger.error(
            f'Failed to fetch addresses with offset {skip} and limit {limit}', exc_info=True)
    return addresses


@app.get("/addresses/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    logger.debug(f'Recieved read request for all address with id {address_id}')
    try:
        db_address = crud.get_address_by_id(db, address_id=address_id)
        logger.debug(f'Found address with id {db_address}')

        if db_address is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Address with id {address_id} not found")
    except Exception as e:
        logger.error(
            f'Failed to fetch address with id {db_address}', exc_info=True)
    return db_address


@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    try:
        db_address = crud.get_address_by_id(db, address_id=address_id)
        if db_address is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Address with id {address_id} not found")
        crud.delete_address_by_id(db, address_id)
    except Exception as e:
        logger.error(
            f'Failed to delete address with id {db_address}', exc_info=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

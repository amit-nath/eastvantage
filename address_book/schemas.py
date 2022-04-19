from pydantic import BaseModel, ValidationError, validator


class AddressBase(BaseModel):
    # value should be float and >= -90 and <= 90
    latitude: float
    # value should be float and >= -180 and <= 180
    longitude: float

    @validator('latitude')
    def latitude_validator(cls, value):
        if value < -90 and value > 90:
            raise ValidationError('value should be float and >= -90 and <= 90')
        return value

    @validator('longitude')
    def longitude_validator(cls, value):
        if value < -180 and value > 180:
            raise ValidationError(
                'value should be float and >= -180 and <= 180')
        return value


class AddressRead(AddressBase):
    pass


class AddressCreate(AddressBase):
    pass


class AddressDelete(AddressBase):
    pass


class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True

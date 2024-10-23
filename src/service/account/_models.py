from pydantic import BaseModel, ConfigDict


class DecodedContent(BaseModel):
    type: str
    comment: str

    model_config = ConfigDict(from_attributes=True)


class MessageContent(BaseModel):
    body: str
    decoded: DecodedContent | None = None
    hash: str

    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    hash: str | None = None
    source: str | None = None
    destination: str | None = None
    value: str | None = None
    fwd_fee: str | None = None
    ihr_fee: str | None = None
    created_at: str | None = None
    created_lt: str | None = None
    opcode: str | None = None
    ihr_disabled: bool | None = None
    bounce: bool | None = None
    bounced: bool | None = None
    import_fee: str | None = None
    message_content: MessageContent | None = None
    init_state: MessageContent | None = None

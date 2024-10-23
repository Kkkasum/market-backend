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


class NftTransfer(BaseModel):
    query_id: str | None = None
    nft_address: str | None = None
    nft_collection: str | None = None
    transaction_hash: str | None = None
    transaction_lt: str | None = None
    transaction_now: int | None = None
    transaction_aborted: bool | None = None
    old_owner: str | None = None
    new_owner: str | None = None
    response_destination: str | None = None
    custom_payload: str | None = None
    forward_amount: str | None = None
    forward_payload: str | None = None
    trace_id: str | None = None

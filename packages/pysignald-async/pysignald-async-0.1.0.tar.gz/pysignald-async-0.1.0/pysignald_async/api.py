import asyncio
import typing

from pysignald_async.error import SignaldException
from pysignald_async.generated import *
import pysignald_async.util as util


@util.nested_dataclass
class Contact:
    name: str = None
    address: JsonAddressv1 = None
    profileKey: str = None
    messageExpirationTime: int = None


@util.nested_dataclass
class Profile:
    name: str = None
    address: JsonAddressv1 = None
    avatar: str = None
    capabilities: dict = None
    identity_key: str = None
    unidentified_access: str = None
    unrestricted_unidentified_access: bool = None


class SignaldAPI(SignaldGeneratedAPI):
    async def get_response_and_wait_for(
        self, request: dict, validator: typing.Callable
    ):
        future = self.get_future_for(validator)
        try:
            await self.get_response(request)
        except SignaldException:
            self.specific_handlers.remove(future.handler)
            future.cancel()
            raise
        else:
            await future

    async def subscribe(self, username: str):
        """
        Starts receiving messages for the account identified by the argument
        username (a phone number).
        """
        await self.get_response_and_wait_for(
            request={"type": "subscribe", "username": username},
            validator=lambda response: response.get("type") == "listen_started"
            and response.get("data") == username,
        )

    async def unsubscribe(self, username: str):
        """
        Stops receiving message for an phone 'username'.
        """
        await self.get_response_and_wait_for(
            request={"type": "unsubscribe", "username": username},
            validator=lambda response: response.get("type") == "listen_stopped"
            and response.get("data") == username,
        )

    async def link(
        self, deviceName: str, username: str
    ) -> typing.Tuple[str, asyncio.Future]:
        """
        Link signald to an existing signal account.

        Return a URI that needs to be converted to a QR code to be scanned with
        the official signal app, and a future which result is set to True once the
        link is successful.
        """
        linking_successful = self.get_future_for(
            lambda response: response.get("type") == "linking_successful"
            and response.get("data", dict()).get("username") == username
        )
        try:
            response = await self.get_response(
                {"type": "link", "deviceName": deviceName}
            )
        except SignaldException:
            self.specific_handlers.remove(linking_successful.handler)
            linking_successful.cancel()
            raise
        else:
            uri = response.get("data", dict()).get("uri")
            return uri, linking_successful

    async def list_contacts(self, username: str) -> typing.List[Contact]:
        contact_list = await self.get_response(
            {"type": "list_contacts", "username": username}
        )
        return [Contact(**c) for c in contact_list]

    async def list_groups(self, username: str) -> typing.List[JsonGroupV2Infov1]:
        response = await self.get_response(
            {"type": "list_groups", "username": username}
        )
        print(response)
        if len(response.get("groups", [])) != 0:
            self.logger.warning("Some groupsV1 were returned, ignoring them")

        return [JsonGroupV2Infov1(**g) for g in response.get("groupsv2")]

    async def get_profile(
        self, username: str, recipientAddress: JsonAddressv1
    ) -> Profile:
        response = await self.get_response(
            {
                "type": "get_profile",
                "username": username,
                "recipientAddress": util.asdict_non_none(recipientAddress),
            }
        )
        return Profile(**response)

    async def verify(self, username: str, code: str):
        await self.get_response_and_wait_for(
            request={"type": "verify", "username": username, "code": code},
            validator=lambda response: response.get("type") == "verified"
            and response.get("data", {}).get("username") == username,
        )

    async def register(self, username: str):
        """
        Register signald as the primary signal device for a phone number.
        To complete to process, the SignaldAPI.verify coroutine must then be
        awaited with the code received by SMS.
        """
        await self.get_response_and_wait_for(
            request={"type": "register", "username": username},
            validator=lambda response: response.get("type") == "verification_required"
            and response.get("data", {}).get("username") == username,
        )

    def handle_message(self, payload):
        envelope = JsonMessageEnvelopev1(**payload.get("data", dict()))
        print(envelope)

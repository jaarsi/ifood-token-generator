import json
from typing import Any

import ifood
import streamlit as st
import settings


class State:
    usercode: ifood.UserCodeResponse
    authorizer: ifood.AuthorizerFunction
    token: ifood.TokenResponse

    def __getattribute__(self, __name: str) -> Any:
        return st.session_state.get(__name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        st.session_state[__name] = __value


state = State()
st.set_page_config(
    page_title="Gerador de Tokens do IFood"
)
st.title(settings.COMPANY_NAME)


def request_usercode_handler():
    try:
        usercode, authorizer = ifood.request_usercode()
    except Exception as error:
        st.error(repr(error))
    else:
        state.usercode = usercode
        state.authorizer = authorizer
        state.token = None


st.subheader("Gerador de Tokens do :red[IFood]")
st.button(":label: Gerar Código", on_click=request_usercode_handler)
c1, c2 = st.columns([.3, .7])
c1.text("Codigo de vinculação")
c1.code(state.usercode["userCode"] if state.usercode else "")
c2.text("URL de vinculação")
c2.code(state.usercode["verificationUrlComplete"] if state.usercode else "")
verification_code_input = st.text_input(
    label="Código de verificação", disabled=(not state.usercode)
)


def authorizer_handler():
    try:
        state.token = state.authorizer(verification_code_input.strip())
    except Exception as error:
        st.error(repr(error))
    else:
        st.success("Token gerado com sucesso!")


c1, c2, *_ = st.columns(4)
c1.button(":key: Autorizar", on_click=authorizer_handler, disabled=(not state.usercode))
c2.download_button(
    ":admission_tickets: Baixar Token",
    json.dumps(state.token, indent=4),
    file_name="token.ifood.json",
    disabled=(not state.token),
    type="primary"
)

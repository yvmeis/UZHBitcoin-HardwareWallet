from src.coins.coin import Coin

from btclib.psbt import (
    PSBT_DELIMITER,
    PSBT_SEPARATOR,
    Psbt,
    combine_psbts,
    extract_tx,
    finalize_psbt
)


class Bitcoin(Coin):

    def sign_transaction(self):
        pass

    def get_transaction_info(self, tx) -> str:
        psbt_raw = Psbt.b64decode(tx)
        psbt_raw.assert_valid()
        psbt_raw.assert_signable()
        psbt: dict = psbt_raw.to_dict()

        vout: list[dict] = psbt["tx"]["vout"]

        text = ""

        for stream in vout:
            text += f"Paying {0.00000001 * stream['value']} btc to {stream['address']}\n"

        return text

    def __str__(self):
        return "Bitcoin"

from src.image_utils import load_image, save_image
from src.steganography import encode_payload, decode_payload, save_stego_image
from src.cryptography import encrypt_message, decrypt_message

def hide_message(image_path, output_path, message, password):
    image = load_image(image_path)

    payload = encrypt_message(message, password)

    output_image = encode_payload(image, payload)

    save_stego_image(output_image, output_path)


def reveal_message(image_path, password):
    image = load_image(image_path)

    try:
        payload = bytes(decode_payload(image))
        message = decrypt_message(payload, password)
        return message

    except Exception as exc:
        raise ValueError(
            f"Message recovery failed during extraction or decryption: "
            f"{type(exc).__name__}: {exc}"
        ) from exc
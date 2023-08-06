from malaya_speech.path import PATH_AGE_DETECTION, S3_PATH_AGE_DETECTION
from malaya_speech.supervised import classification
from herpetologist import check_type

_availability = {
    'vggvox-v2': {
        'Size (MB)': 30.9,
        'Quantized Size (MB)': 7.92,
        'Accuracy': 0.57523,
    },
    'deep-speaker': {
        'Size (MB)': 96.9,
        'Quantized Size (MB)': 24.4,
        'Accuracy': 0.58584,
    },
}

labels = [
    'teens',
    'twenties',
    'thirties',
    'fourties',
    'fifties',
    'sixties',
    'seventies',
    'eighties',
    'nineties',
    'not an age',
]


def available_model():
    """
    List available age detection deep models.
    """
    from malaya_speech.utils import describe_availability

    return describe_availability(
        _availability,
        text = 'last accuracy during training session before early stopping.',
    )


@check_type
def deep_model(model: str = 'vggvox-v2', quantized: bool = False, **kwargs):
    """
    Load age detection deep model.

    Parameters
    ----------
    model : str, optional (default='vggvox-v2')
        Model architecture supported. Allowed values:

        * ``'vggvox-v2'`` - finetuned VGGVox V2.
        * ``'deep-speaker'`` - finetuned Deep Speaker.
    quantized : bool, optional (default=False)
        if True, will load 8-bit quantized model. 
        Quantized model not necessary faster, totally depends on the machine.

    Returns
    -------
    result : malaya_speech.supervised.classification.load function
    """

    model = model.lower()
    if model not in _availability:
        raise Exception(
            'model not supported, please check supported models from `malaya_speech.age_detection.available_model()`.'
        )

    settings = {
        'vggvox-v2': {'concat': False},
        'deep-speaker': {'voice_only': False},
    }

    return classification.load(
        path = PATH_AGE_DETECTION,
        s3_path = S3_PATH_AGE_DETECTION,
        model = model,
        name = 'age-detection',
        extra = settings[model],
        label = labels,
        quantized = quantized,
        **kwargs
    )

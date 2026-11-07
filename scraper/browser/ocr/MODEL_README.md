---
license: apache-2.0
library_name: onnxruntime
tags:
- ocr
- paddleocr
- onnx
- onnxruntime-web
---

# PP-OCRv5 mobile (ONNX, for browsers)

ONNX versions of three [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) PP-OCRv5 models, for running in the browser with onnxruntime-web.
They are used by the inference tab of [IIIF Kasane](https://kasane.ldas.jp).

| File | Original | What it does |
|---|---|---|
| `PP-OCRv5_mobile_det.onnx` | [PaddlePaddle/PP-OCRv5_mobile_det](https://huggingface.co/PaddlePaddle/PP-OCRv5_mobile_det) (rev 0d63e78) | Finds text lines (DB) |
| `PP-OCRv5_mobile_rec.onnx` | [PaddlePaddle/PP-OCRv5_mobile_rec](https://huggingface.co/PaddlePaddle/PP-OCRv5_mobile_rec) (rev 682f205) | Reads a line: Simplified and Traditional Chinese, English, Japanese (CTC, 18,385 classes) |
| `latin_PP-OCRv5_mobile_rec.onnx` | [PaddlePaddle/latin_PP-OCRv5_mobile_rec](https://huggingface.co/PaddlePaddle/latin_PP-OCRv5_mobile_rec) (rev ab2cd5c) | Reads a line in Latin-script languages (CTC, 838 classes) |

`*.dict.json` is the `character_dict` of each recognizer's `inference.yml`, as a JSON array. Class 0 is the CTC blank, class k + 1 is `dict[k]`, and the last class is a space.

## Conversion

The weights are unchanged (float32). Converted with paddle2onnx 2.1.0 (PaddlePaddle 3.3.1):

```
paddle2onnx --model_dir <model> --model_filename inference.json --params_filename inference.pdiparams --save_file <model>.onnx --opset_version 14
```

On random input, the ONNX outputs (onnxruntime 1.31, CPU) differ from Paddle inference by at most 1.3e-7 (detector) and 7.2e-5 (recognizer).
On one printed English page (Internet Archive, *Origin of Species*, page 30, 1234 × 2048), a TypeScript port of the pipeline found the same 42 lines as PaddleOCR 3.7.0; 40 lines read identically, 3 of 2,266 characters differ.

## License

Apache License 2.0, as the original models. Original models: PaddlePaddle Authors. Conversion: Satoru Nakamura (The University of Tokyo).

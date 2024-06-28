i add some custom scripts i use with whisper.cpp in this branch and some enhancements to deprecated scripts

## Core ML support

On Apple Silicon devices, the Encoder inference can be executed on the Apple Neural Engine (ANE) via Core ML. This can result in significant
speed-up - more than x3 faster compared with CPU-only execution. Here are the instructions for generating a Core ML model and using it with `whisper.cpp`:

- Create Python environment and activate it
- Install Python dependencies needed for the creation of the Core ML model:

  ```bash
  pip install --upgrade pip
  pip install ane_transformers  openai-whisper coremltools
  ```

  - To ensure `coremltools` operates correctly, please confirm that [Xcode](https://developer.apple.com/xcode/) is installed and execute `xcode-select --install` to install the command-line tools.
  - Python 3.10 is recommended.
  - MacOS Sonoma (version 14) or newer is recommended, as older versions of MacOS might experience issues with transcription hallucination.

- Generate a Core ML model. For example, to generate a `base.en` model, use:

  ```bash
  ./models/generate-coreml-model.sh base.en
  ```

  This will generate the folder `models/ggml-base.en-encoder.mlmodelc`

- Build `whisper.cpp` with Core ML support:

  ```bash
  # using Makefile
  make clean
  WHISPER_COREML=1 make -j

  # using CMake
  cmake -B build -DWHISPER_COREML=1
  cmake --build build -j --config Release
  ```

- Run the examples as usual. For example:

  ```bash
  ./main -m models/ggml-base.en.bin -f samples/jfk.wav
  ```

  ```bash
  ...

  whisper_init_state: loading Core ML model from 'models/ggml-base.en-encoder.mlmodelc'
  whisper_init_state: first run on a device may take a while ...
  whisper_init_state: Core ML model loaded

  system_info: n_threads = 4 / 10 | AVX = 0 | AVX2 = 0 | AVX512 = 0 | FMA = 0 | NEON = 1 | ARM_FMA = 1 | F16C = 0 | FP16_VA = 1 | WASM_SIMD = 0 | BLAS = 1 | SSE3 = 0 | VSX = 0 | COREML = 1 |

  ...
  ```

  The first run on a device is slow, since the ANE service compiles the Core ML model to some device-specific format.
  Next runs are faster.

For more information about the Core ML implementation please refer to PR [#566](https://github.com/ggerganov/whisper.cpp/pull/566).

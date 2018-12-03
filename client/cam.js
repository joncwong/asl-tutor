(env => {
  const ML_API_URL = "Your local machine ";

  navigator.getUserMedia =
    navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia;

  function getPrediction(imageDataUrl) {
    var formData = new FormData();
    formData.append("image", imageDataUrl)
    return fetch(`${ML_API_URL + "api path here"}`, {
      method: "POST",
      body: formData
    })
      .then(res => {
        return res.json();
      })
      .then(data => {
        return data;
      });
  }

  function captureVideoFrame(canvas) {
    return canvas.toDataURL("image/jpeg");
  }

  function clearCanvas(canvas) {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, c.height);
  }

  function drawRect(canvas, x, y, width, height, color = "#000080") {
    const ctx = canvas.getContext("2d");

    ctx.beginPath();
    ctx.globalAlpha = 1.0;
    ctx.lineWidth = 2;
    ctx.strokeStyle = color;
    ctx.strokeRect(x, y, width, height);
  }

  /**
   * Main app things
   */
  function App() {
    const videoElem = document.querySelector
    ("#video-container video");
    const captionElem = document.querySelector(".caption");
    const canvas = document.querySelector("#video-container > canvas");

    /**
     * Stateful things
     */
    const state = {
      predictionLoop: undefined,
      captionText: "Prediction from input here"
    };

    const setCaptionText = text => {
      state.captionText = text;
      captionElem.textContent = state.captionText;
    };

    const startPredictionLoop = () => {
      state.predictionLoop = setInterval(() => {
        const imageDataUrl = captureVideoFrame(canvas);
        getPrediction(imageDataUrl)
          .then(data => {
            clearCanvas(canvas);
            state.captionText = data.prediction;
            captionElem.textContent = state.captionText;
          })
          .catch(() => {
            stopPredictionLoop();
          });
      }, 200);
    };

    const stopPredictionLoop = () => {
      clearInterval(state.predictionLoop);
    };

    const initialise = () => {
      navigator.getUserMedia(
        {
          video: true
        },
        stream => {
          console.info("got stream", stream);
          videoElem.srcObject = stream;

          // configure a fake presentation for demo purposes
          if (env === "demo") {
              drawRect(canvas, 200, 250, 230, 170);
              setCaptionText("Prediction from input here");
          } else {
            startPredictionLoop();
          }
        },
        err => console.error(err)
      );
    };

    return {
      initialise
    };
  }

  const app = App();
  app.initialise();
})("run");

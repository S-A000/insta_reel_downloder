let lastVideoUrl = "";

chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    // Mazeed broad checking: mp4, video data, ya instagram cdn links
    if (details.url.includes(".mp4") || 
        details.url.includes("video_dash") || 
        (details.url.includes("cdninstagram.com") && details.url.includes("_v.mp4"))) {
      
      console.log("Video Detected:", details.url);
      lastVideoUrl = details.url;
      chrome.storage.local.set({ latestReelUrl: lastVideoUrl });
    }
  },
  { urls: ["<all_urls>"] }, // Sab urls check karein taake koi miss na ho
  ["requestBody"]
);
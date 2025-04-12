import { exec } from "child_process";

const checkApiStatus = async () => {
  const maxRetries = 5;
  const baseDelay = 1000; // 1 second

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const isAlive = await fetch("http://localhost:8000/api/v1/hello")
      .then((res) => res?.ok)
      .catch(() => false);

    if (isAlive) {
      return true;
    }

    if (attempt === maxRetries - 1) {
      throw new Error("Make sure Core API is running at http://localhost:8000");
    }

    // Linear backoff: wait longer with each attempt
    const delay = baseDelay * (attempt + 1);
    console.log(
      `API not available, retrying in ${delay / 1000}s (attempt ${
        attempt + 1
      }/${maxRetries})...`
    );
    await new Promise((resolve) => setTimeout(resolve, delay));
  }
};

export const generateApiClient = async () => {
  try {
    await checkApiStatus();

    exec(
      "pnpm dlx openapi-typescript http://localhost:8000/openapi.json -o ./src/generated.ts"
    );

    console.log("API client generated successfully");
  } catch (error) {
    if (error instanceof Error) {
      console.error(`Error: ${error.message}`);
    } else {
      console.error(`Error: ${error}`);
    }
  }
};

generateApiClient();

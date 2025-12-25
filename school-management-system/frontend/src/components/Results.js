import React, { useEffect, useState } from "react";
import { getResults } from "../services/dataService";

const Results = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await getResults();
        setResults(data);
        setLoading(false);
      } catch (err) {
        console.error("Error fetching results data:", err);
        setError("Failed to load results data. Please try again later.");
        setLoading(false);
      }
    };

    fetchResults();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h1>Results</h1>
      <pre>{JSON.stringify(results, null, 2)}</pre>
    </div>
  );
};

export default Results;

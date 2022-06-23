import { useState, useEffect, useCallback } from "react";

import { fetchApi } from "@util/comm-util";

export default function MainPage() {
  const [results, setResults] = useState<any>([]);

  const fetchMovies = useCallback(async () => {
    const res = await fetchApi(
      `https://api.themoviedb.org/3/movie/popular?api_key=22478a88b22311a5249584b2c23d6a3d`
    );

    setResults(res.results);
  }, []);

  useEffect(() => {
    fetchMovies();
  }, [fetchMovies]);

  return (
    <div className="px-4 pt-1">
      <div className="md:columns-2 2xl:columns-3 gap-10 [column-fill:_balance] box-border mx-auto before:box-inherit after:box-inherit">
        {results &&
          results.map((m: any, index: number) => (
            <div
              key={index}
              className="p-8 mb-6 shadow-xl break-inside-avoid card bg-base-100"
            >
              <figure>
                <img
                  src={`https://image.tmdb.org/t/p/w185${m.poster_path}`}
                  alt="Shoes"
                />
              </figure>
              <div className="card-body">
                <h2 className="card-title">{m.title}</h2>
                <p>{m.overview}</p>
                <div className="justify-end card-actions">
                  <button className="btn btn-primary">Buy Now</button>
                </div>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}

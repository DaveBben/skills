chi.Walk missing routes

Similarly to https://github.com/go-chi/chi/issues/750, I'm trying to use chi.Walk() to get a report of all routes. However, I found that some routes are missing when I use Route() as well as e.g. Get() with the same pattern: https://go.dev/play/p/7Ntz1yMoXrz

Interestingly, the route _is_ visited by the walk function when you change `r.Route("/bar", ...` to `r.Route("/bar/", ...`.

Since the `GET /foo/bar` request is handled in both cases, I also expect chi.Walk() to report the route in both cases.


The playground program at that link:

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"

	"github.com/go-chi/chi/v5"
)

func main() {
	r := chi.NewRouter()

	r.Route("/foo", func(r chi.Router) {
		r.Route("/bar", func(r chi.Router) {
			r.Get("/{id}", func(w http.ResponseWriter, r *http.Request) { fmt.Fprintln(w, "handler for /foo/bar/{id}") })
		})
		r.Get("/bar", func(w http.ResponseWriter, r *http.Request) { fmt.Fprintln(w, "handler for /foo/bar") })
	})

	fmt.Println("routes as reported by chi.Walk:")

	walkFunc := func(method string, route string, _ http.Handler, _ ...func(http.Handler) http.Handler) error {
		fmt.Println(method, route)
		return nil
	}

	if err := chi.Walk(r, walkFunc); err != nil {
		panic(err)
	}

	fmt.Println("proof that GET /foo/bar is handled:")

	s := httptest.NewServer(r)
	defer s.Close()

	resp, err := http.Get(s.URL + "/foo/bar")
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}

	fmt.Print(string(body))
}
-- go.mod --
module play.ground
```

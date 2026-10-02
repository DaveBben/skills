`chi.Walk()` misses routes when a handler shares its pattern with a `Route()` or `Mount()`.

I use `chi.Walk()` to print a report of every route the router serves. Some routes are missing from it. Here is a reproduction:

```go
r := chi.NewRouter()
r.Route("/foo", func(r chi.Router) {
    r.Route("/bar", func(r chi.Router) {
        r.Get("/{id}", h)
    })
    r.Get("/bar", h)
})
chi.Walk(r, func(method, route string, handler http.Handler, mws ...func(http.Handler) http.Handler) error {
    fmt.Println(method, route)
    return nil
})
```

This prints `GET /foo/bar/{id}` but not `GET /foo/bar`, although a `GET /foo/bar` request is served by `h`. When I change `r.Route("/bar", ...)` to `r.Route("/bar/", ...)`, `GET /foo/bar` does appear.

Expected: every route the router actually serves appears in `Walk()`, and in `Routes()`, whichever of the two forms I use. Routing itself already works and must not change.

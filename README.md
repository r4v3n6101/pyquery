# vquery
Rust crate is helpful at querying information from Valve's goldsrc/source servers (both are supported).

## Use example
```rust
let query = ValveQuery::<SourceParser>::bind("0.0.0.0:0".parse().unwrap()).unwrap();
query.connect(ADDR).unwrap();
let info = query.a2s_info_new().unwrap();
// and other a2s data
```

## TO-DO list
- [x] **single packet**: Parse single (i.e. only 1400 bytes) packet.
- [x] **goldsrc multi packet**: Parse multi packet using goldsrc scheme.
- [x] **source multi**: Same as above but with source protocol.
- [x] **a2s data**: Acquire a2s data.
- [x] **bz2 decompression**: Decompress source multipacket data with bzip2 crate.
- [x] **crc32**: Verify that data is correct using crc32 of decompressed data.
- [ ] **documentation**: There're no docs absolutely!
- [ ] **normal visibility of modules/structs/traits**: As for me, pub modifiers are bad located for now.
- [x] **master server query**: Seems it works correctly.

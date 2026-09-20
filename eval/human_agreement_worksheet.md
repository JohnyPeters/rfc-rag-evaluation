# Folha de anotacao humana - concordancia juiz-humano

20 perguntas, amostra estratificada por categoria (proporcional as 41 respondidas).

Preenche os campos TEU_VEREDICTO. Decide antes de veres o veredicto do juiz (results/validity_c3/judge_metrics.json).

---

## q001 (direct_factual)

**Pergunta:** What does a 404 status code indicate about a resource?

**Resposta gerada:** A 404 status code indicates that the origin server did not find a current representation for the target resource or is not willing to disclose that one exists. RFC 9110 §15.5.5

**Gabarito:** The origin server did not find a current representation for the target resource, or is not willing to disclose that one exists.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9110 §15.5.5]
§15.5.5 404 Not Found

The 404 (Not Found) status code indicates that the origin server did
   not find a current representation for the target resource or is not
   willing to disclose that one exists.  A 404 status code does not
   indicate whether this lack of representation is temporary or
   permanent; the 410 (Gone) status code is preferred over 404 if the
   origin server knows, presumably through some configurable means, that
   the condition is likely to be permanent.

   A 404 response is heuristically cacheable; i.e., unless otherwise
   indicated by the method definition or explicit cache controls (see
   Section 4.2.2 of [CACHING]).

[RFC 9110 §15.5.11]
§15.5.11 410 Gone

The 410 (Gone) status code indicates that access to the target
   resource is no longer available at the origin server and that this
   condition is likely to be permanent.  If the origin server does not
   know, or has no facility to determine, whether or not the condition
   is permanent, the status code 404 (Not Found) ought to be used
   instead.

   The 410 response is primarily intended to assist the task of web
   maintenance by notifying the recipient that the resource is
   intentionally unavailable and that the server owners desire that
   remote links to that resource be removed.  Such an event is common
   for limited-time, promotional services and for resources belonging to
   individuals no longer associated with the origin server's site.  It
   is not necessary to mark all p

[RFC 9110 §16.2.2]
§16.2.2 Considerations for New Status Codes

can mandate a zero-length content.

   Proposals for new status codes that are not yet widely deployed ought
   to avoid allocating a specific number for the code until there is
   clear consensus that it will be registered; instead, early drafts can
   use a notation such as "4NN", or "3N0" .. "3N9", to indicate the
   class of the proposed status code(s) without consuming a number
   prematurely.

   The definition of a new status code ought to explain the request
   conditions that would cause a response containing that status code
   (e.g., combinations of request header fields and/or method(s)) along
   with any dependencies on response header fields (e.g., what fields
   are required, what fields can modify the semantics, and what field
   semantics are further refined when used with

[RFC 9110 §16.2.2]
§16.2.2 Considerations for New Status Codes

header fields (e.g., what fields
   are required, what fields can modify the semantics, and what field
   semantics are further refined when used with the new status code).

   By default, a status code applies only to the request corresponding
   to the response it occurs within.  If a status code applies to a
   larger scope of applicability -- for example, all requests to the
   resource in question or all requests to a server -- this must be
   explicitly specified.  When doing so, it should be noted that not all
   clients can be expected to co
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q003 (direct_factual)

**Pergunta:** What must a cache not do when a request or response carries the no-store directive?

**Resposta gerada:** A cache MUST NOT store any part of either the immediate request or the response when a request or response carries the no-store directive. It MUST also make a best-effort attempt to remove the information from volatile storage as promptly as possible after forwarding it. 

RFC 9111 §5.2.1.5, RFC 9111 §5.2.2.5

**Gabarito:** A cache must not store any part of either the request or any response to it, in either private or shared caches.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9111 §5.2.2.5]
§5.2.2.5 no-store

The no-store response directive indicates that a cache MUST NOT store
   any part of either the immediate request or the response and MUST NOT
   use the response to satisfy any other request.

   This directive applies to both private and shared caches.  "MUST NOT
   store" in this context means that the cache MUST NOT intentionally
   store the information in non-volatile storage and MUST make a best-
   effort attempt to remove the information from volatile storage as
   promptly as possible after forwarding it.

   This directive is not a reliable or sufficient mechanism for ensuring
   privacy.  In particular, malicious or compromised caches might not
   recognize or obey this directive, and communications networks might
   be vulnerable to eavesdropping.

   Note that the must-understand cache directive overrides no-store in
   certain circumstances; see Section 5.2.2.3.

[RFC 9111 §5.2.1.5]
§5.2.1.5 no-store

The no-store request directive indicates that a cache MUST NOT store
   any part of either this request or any response to it.  This
   directive applies to both private and shared caches.  "MUST NOT
   store" in this context means that the cache MUST NOT intentionally
   store the information in non-volatile storage and MUST make a best-
   effort attempt to remove the information from volatile storage as
   promptly as possible after forwarding it.

   This directive is not a reliable or sufficient mechanism for ensuring
   privacy.  In particular, malicious or compromised caches might not
   recognize or obey this directive, and communications networks might
   be vulnerable to eavesdropping.

   Note that if a request containing this directive is satisfied from a
   cache, the no-store request directive does not apply to the already
   stored response.

[RFC 9111 §3]
§3 Storing Responses in Caches

A cache MUST NOT store a response to a request unless:

   *  the request method is understood by the cache;

   *  the response status code is final (see Section 15 of [HTTP]);

   *  if the response status code is 206 or 304, or the must-understand
      cache directive (see Section 5.2.2.3) is present: the cache
      understands the response status code;

   *  the no-store cache directive is not present in the response (see
      Section 5.2.2.5);

   *  if the cache is shared: the private response directive is either
      not present or allows a shared cache to store a modified response;
      see Section 5.2.2.7);

   *  if the cache is shared: the Authorization header field is not
      present in the request (see Section 11.6.2 of [HTTP]) or a
      response directive is present 

[RFC 9111 §5.2.2.3]
§5.2.2.3 must-understand

The must-understand response directive limits caching of the response
   to a cache that understands and conforms to the requirements for that
   response's status code.

   A response that contains the must-understand directive SHOULD also
   contain the no-store di
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q005 (direct_factual)

**Pergunta:** What are the two tables HPACK uses to associate header fields with indexes?

**Resposta gerada:** The two tables HPACK uses to associate header fields with indexes are the static table (see Section 2.3.1) and the dynamic table (see Section 2.3.2). RFC 7541 §2.3

**Gabarito:** A static table, which is predefined and contains common header fields, and a dynamic table, which the encoder builds up to index header fields repeated within the encoded header lists.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 7541 §2.3]
§2.3 Indexing Tables

HPACK uses two tables for associating header fields to indexes.  The
   static table (see Section 2.3.1) is predefined and contains common
   header fields (most of them with an empty value).  The dynamic table
   (see Section 2.3.2) is dynamic and can be used by the encoder to
   index header fields repeated in the encoded header lists.

   These two tables are combined into a single address space for
   defining index values (see Section 2.3.3).

[RFC 9204 §2]
§2 Compression Process Overview

Like HPACK, QPACK uses two tables for associating field lines
   ("headers") to indices.  The static table (Section 3.1) is predefined
   and contains common header field lines (some of them with an empty
   value).  The dynamic table (Section 3.2) is built up over the course
   of the connection and can be used by the encoder to index both header
   and trailer field lines in the encoded field sections.

   QPACK defines unidirectional streams for sending instructions from
   encoder to decoder and vice versa.

[RFC 9204 §3]
§3 Reference Tables

Unlike in HPACK, entries in the QPACK static and dynamic tables are
   addressed separately.  The following sections describe how entries in
   each table are addressed.

[RFC 7541 §2.1]
§2.1 Header List Ordering

HPACK preserves the ordering of header fields inside the header list.
   An encoder MUST order header field representations in the header
   block according to their ordering in the original header list.  A
   decoder MUST order header fields in the decoded header list according
   to their ordering in the header block.

[RFC 7541 §1.1]
§1.1 Overview

The format defined in this specification treats a list of header
   fields as an ordered collection of name-value pairs that can include
   duplicate pairs.  Names and values are considered to be opaque
   sequences of octets, and the order of header fields is preserved
   after being compressed and decompressed.

   Encoding is informed by header field tables that map header fields to
   indexed values.  These header field tables can be incrementally
   updated as new header fields are encoded or decoded.

   In the encoded form, a header field is represented either literally
   or as a reference to a header field in one of the header field
   tables.  Therefore, a list of header fields can be encoded using a
   mixture of references and literal values.

   Literal values are either encod

[RFC 7541 §1]
§1 Introduction

ressor that eliminates
   redundant header fields, limits vulnerability to known security
   attacks, and has a bounded memory requirement for use in constrained
   environments.  Potential security concerns for HPACK are described in
   Section 7.

   The HPACK format is intentionally simple and inflexible.  Both
   characteristics reduce the risk of interoperability or security
   issues due to implementation error.  No extensibility mechanisms are
   defined; changes to the format are only possible b
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q007 (direct_factual)

**Pergunta:** What does the Secure attribute limit about a cookie's scope?

**Resposta gerada:** The Secure attribute limits the scope of the cookie to "secure" channels (where "secure" is defined by the user agent). RFC 6265 §4.1.2.5

**Gabarito:** It limits the cookie to secure channels: the user agent includes the cookie in a request only if that request is transmitted over a secure channel, typically HTTP over TLS.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 6265 §4.1.2.5]
§4.1.2.5 The Secure Attribute

The Secure attribute limits the scope of the cookie to "secure"
   channels (where "secure" is defined by the user agent).  When a
   cookie has the Secure attribute, the user agent will include the
   cookie in an HTTP request only if the request is transmitted over a
   secure channel (typically HTTP over Transport Layer Security (TLS)
   [RFC2818]).

   Although seemingly useful for protecting cookies from active network
   attackers, the Secure attribute protects only the cookie's
   confidentiality.  An active network attacker can overwrite Secure
   cookies from an insecure channel, disrupting their integrity (see
   Section 8.6 for more details).

[RFC 6265 §4.1.2.6]
§4.1.2.6 The HttpOnly Attribute

The HttpOnly attribute limits the scope of the cookie to HTTP
   requests.  In particular, the attribute instructs the user agent to
   omit the cookie when providing access to cookies via "non-HTTP" APIs
   (such as a web browser API that exposes cookies to scripts).

   Note that the HttpOnly attribute is independent of the Secure
   attribute: a cookie can have both the HttpOnly and the Secure
   attribute.

[RFC 6265 §5.3]
§5.3 Storage Model

       the default-path of the request-uri.

   8.   If the cookie-attribute-list contains an attribute with an
        attribute-name of "Secure", set the cookie's secure-only-flag to
        true.  Otherwise, set the cookie's secure-only-flag to false.

   9.   If the cookie-attribute-list contains an attribute with an
        attribute-name of "HttpOnly", set the cookie's http-only-flag to
        true.  Otherwise, set the cookie's http-only-flag to false.








   10.  If the cookie was received from a "non-HTTP" API and the
        cookie's http-only-flag is set, abort these steps and ignore the
        cookie entirely.

   11.  If the cookie store contains a cookie with the same name,
        domain, and path as the newly created cookie:

        1.  Let old-cookie be the existing 

[RFC 6265 §4.1.2.4]
§4.1.2.4 The Path Attribute

The scope of each cookie is limited to a set of paths, controlled by
   the Path attribute.  If the server omits the Path attribute, the user
   agent will use the "directory" of the request-uri's path component as
   the default value.  (See Section 5.1.4 for more details.)

   The user agent will include the cookie in an HTTP request only if the
   path portion of the request-uri matches (or is a subdirectory of) the
   cookie's Path attribute, where the %x2F ("/") character is
   interpreted as a directory separator.

   Although seemingly useful for isolating cookies between different
   paths within a given host, the Path attribute cannot be relied upon
   for security (see Section 8).

[RFC 6265 §8.3]
§8.3 Clear Text

the cookies over a secure channel).
   However, encrypting and signing cookie contents does not prevent an
   attacker from transplanting a cookie from one user agent to another
   or from replayin
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q009 (direct_factual)

**Pergunta:** Why does RFC 9111 deprecate the Pragma header field?

**Resposta gerada:** RFC 9111 deprecates the Pragma header field because support for Cache-Control is now widespread.

**Gabarito:** Pragma was defined for HTTP/1.0 caches, before Cache-Control existed, so clients could request "no-cache". Support for Cache-Control is now widespread, so Pragma is deprecated.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9111 §5.4]
§5.4 Pragma

The "Pragma" request header field was defined for HTTP/1.0 caches, so
   that clients could specify a "no-cache" request (as Cache-Control was
   not defined until HTTP/1.1).

   However, support for Cache-Control is now widespread.  As a result,
   this specification deprecates Pragma.

      |  *Note:* Because the meaning of "Pragma: no-cache" in responses
      |  was never specified, it does not provide a reliable replacement
      |  for "Cache-Control: no-cache" in them.

[RFC 9110 §18.4]
§18.4 Field Name Registration

--------------------+------------+---------+------------+
   | *                         | permanent  | 12.5.5  | (reserved) |
   +---------------------------+------------+---------+------------+

                                Table 9

   The field name "*" is reserved because using that name as an HTTP
   header field might conflict with its special semantics in the Vary
   header field (Section 12.5.5).

   IANA has updated the "Content-MD5" entry in the new registry to have
   a status of 'obsoleted' with references to Section 14.15 of [RFC2616]
   (for the definition of the header field) and Appendix B of [RFC7231]
   (which removed the field definition from the updated specification).

[RFC 9110 §1.4]
§1.4 Specifications Obsoleted by This Document

       | [RFC7232] | B.4 |
   +--------------------------------------------+-----------+-----+
   | HTTP/1.1 Range Requests                    | [RFC7233] | B.5 |
   +--------------------------------------------+-----------+-----+
   | HTTP/1.1 Authentication                    | [RFC7235] | B.6 |
   +--------------------------------------------+-----------+-----+
   | HTTP Status Code 308 (Permanent Redirect)  | [RFC7538] | B.7 |
   +--------------------------------------------+-----------+-----+
   | HTTP Authentication-Info and Proxy-        | [RFC7615] | B.8 |
   | Authentication-Info Response Header Fields |           |     |
   +--------------------------------------------+-----------+-----+
   | HTTP Client-Initiated Content-Encoding     | [RFC7694] | B.9 |
   +---------------------

[RFC 9114 §12.1]
§12.1 Normative References

., Ed., Nottingham, M., Ed., and J. Reschke,
              Ed., "HTTP Caching", STD 98, RFC 9111,
              DOI 10.17487/RFC9111, June 2022,
              <https://www.rfc-editor.org/info/rfc9111>.

   [HTTP-REPLAY]
              Thomson, M., Nottingham, M., and W. Tarreau, "Using Early
              Data in HTTP", RFC 8470, DOI 10.17487/RFC8470, September
              2018, <https://www.rfc-editor.org/info/rfc8470>.

   [QPACK]    Krasic, C., Bishop, M., and A. Frindell, Ed., "QPACK:
              Field Compression for HTTP/3", RFC 9204,
              DOI 10.17487/RFC9204, June 2022,
              <https://www.rfc-editor.org/info/rfc9204>.

   [QUIC-TRANSPORT]
              Iyengar, J., Ed. and M. Thomson, Ed., "QUIC: A UDP-Based
              Multiplexed and Secure Transport", RFC 9

[RFC 9113 §12 / RFC 9113 
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q011 (direct_factual)

**Pergunta:** Why are unconstrained multiple range requests a denial-of-service concern?

**Resposta gerada:** Unconstrained multiple range requests are a denial-of-service concern because the effort required to request many overlapping ranges of the same data is tiny compared to the time, memory, and bandwidth consumed by attempting to serve the requested data in many parts. RFC 9110 §17.15

**Gabarito:** The effort required to request many overlapping ranges of the same data is tiny compared to the time, memory and bandwidth the server consumes trying to serve the requested data in many parts.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9110 §17.15]
§17.15 Denial-of-Service Attacks Using Range

Unconstrained multiple range requests are susceptible to denial-of-
   service attacks because the effort required to request many
   overlapping ranges of the same data is tiny compared to the time,
   memory, and bandwidth consumed by attempting to serve the requested
   data in many parts.  Servers ought to ignore, coalesce, or reject
   egregious range requests, such as requests for more than two
   overlapping ranges or for many small ranges in a single set,
   particularly when the ranges are requested out of order for no
   apparent reason.  Multipart range requests are not designed to
   support random access.

[RFC 9114 §10.5]
§10.5 Denial-of-Service Considerations

ression -- have legitimate uses.  These features become a
   burden only when they are used unnecessarily or to excess.

   An endpoint that does not monitor such behavior exposes itself to a
   risk of denial-of-service attack.  Implementations SHOULD track the
   use of these features and set limits on their use.  An endpoint MAY
   treat activity that is suspicious as a connection error of type
   H3_EXCESSIVE_LOAD, but false positives will result in disrupting
   valid connections and requests.

[RFC 9113 §10.5]
§10.5 Denial-of-Service Considerations


   A number of HTTP/2 implementations were found to be vulnerable to
   denial of service [NFLX-2019-002].  Below is a list of known ways
   that implementations might be subject to denial-of-service attacks:

   *  Inefficient tracking of outstanding outbound frames can lead to
      overload if an adversary can cause large numbers of frames to be
      enqueued for sending.  A peer could use one of several techniques
      to cause large numbers of frames to be generated:

      -  Providing tiny increments to flow control in WINDOW_UPDATE
         frames can cause a sender to generate a large number of DATA
         frames.

      -  An endpoint is required to respond to a PING frame.

      -  Each SETTINGS frame requires acknowledgment.

      -  An invalid request (or server push) c

[RFC 9110 §15.5.17]
§15.5.17 416 Range Not Satisfiable

The 416 (Range Not Satisfiable) status code indicates that the set of
   ranges in the request's Range header field (Section 14.2) has been
   rejected either because none of the requested ranges are satisfiable
   or because the client has requested an excessive number of small or
   overlapping ranges (a potential denial of service attack).

   Each range unit defines what is required for its own range sets to be
   satisfiable.  For example, Section 14.1.2 defines what makes a bytes
   range set satisfiable.

   A server that generates a 416 response to a byte-range request SHOULD
   generate a Content-Range header field specifying the current length
   of the selected representation (Section 14.4).

   For example:

   HTTP/1.1 416 Range Not Satisfiable
   Date: Fri, 20 Jan 2012 15:41:

[RFC 9113 §10.5]
§10.5 Denial-
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q013 (identifier_lookup)

**Pergunta:** What status code tells a client the server refuses to continue with the current protocol but might upgrade?

**Resposta gerada:** 426 (Upgrade Required) RFC 9110 §15.5.22

**Gabarito:** 426 Upgrade Required. The server must also send an Upgrade header field naming the required protocol(s).

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9110 §15.5.22]
§15.5.22 426 Upgrade Required

The 426 (Upgrade Required) status code indicates that the server
   refuses to perform the request using the current protocol but might
   be willing to do so after the client upgrades to a different
   protocol.  The server MUST send an Upgrade header field in a 426
   response to indicate the required protocol(s) (Section 7.8).

   Example:

   HTTP/1.1 426 Upgrade Required
   Upgrade: HTTP/3.0
   Connection: Upgrade
   Content-Length: 53
   Content-Type: text/plain

   This service requires use of the HTTP/3.0 protocol.

[RFC 9110 §15.2.2]
§15.2.2 101 Switching Protocols

The 101 (Switching Protocols) status code indicates that the server
   understands and is willing to comply with the client's request, via
   the Upgrade header field (Section 7.8), for a change in the
   application protocol being used on this connection.  The server MUST
   generate an Upgrade header field in the response that indicates which
   protocol(s) will be in effect after this response.

   It is assumed that the server will only agree to switch protocols
   when it is advantageous to do so.  For example, switching to a newer
   version of HTTP might be advantageous over older versions, and
   switching to a real-time, synchronous protocol might be advantageous
   when delivering resources that use such features.

[RFC 9110 §7.8]
§7.8 Upgrade

ent cannot begin using an upgraded protocol on the connection
   until it has completely sent the request message (i.e., the client
   can't change the protocol it is sending in the middle of a message).
   If a server receives both an Upgrade and an Expect header field with
   the "100-continue" expectation (Section 10.1.1), the server MUST send
   a 100 (Continue) response before sending a 101 (Switching Protocols)
   response.

   The Upgrade header field only applies to switching protocols on top
   of the existing connection; it cannot be used to switch the
   underlying connection (transport) protocol, nor to switch the
   existing communication to a different connection.  For those
   purposes, it is more appropriate to use a 3xx (Redirection) response
   (Section 15.4).

   This sp

[RFC 9110 §7.8]
§7.8 Upgrade

st.

   The following is a hypothetical example sent by a client:

   GET /hello HTTP/1.1
   Host: www.example.com
   Connection: upgrade
   Upgrade: websocket, IRC/6.9, RTA/x11

   The capabilities and nature of the application-level communication
   after the protocol change is entirely dependent upon the new
   protocol(s) chosen.  However, immediately after sending the 101
   (Switching Protocols) response, the server is expected to continue
   responding to the original request as if it had received its
   equivalent within the new protocol (i.e., the server still has an
   outstanding request to satisfy after the protocol has been changed,
   and is expected to do so without requiring the request to be
   repeated).

   For example, if the Upgrade header
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q016 (identifier_lookup)

**Pergunta:** What frame type value identifies a SETTINGS frame in HTTP/2?

**Resposta gerada:** 0x04 (RFC 9113 §4.1)

**Gabarito:** Type=0x04.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9114 §7.2.4]
§7.2.4 SETTINGS

The SETTINGS frame (type=0x04) conveys configuration parameters that
   affect how endpoints communicate, such as preferences and constraints
   on peer behavior.  Individually, a SETTINGS parameter can also be
   referred to as a "setting"; the identifier and value of each setting
   parameter can be referred to as a "setting identifier" and a "setting
   value".

   SETTINGS frames always apply to an entire HTTP/3 connection, never a
   single stream.  A SETTINGS frame MUST be sent as the first frame of
   each control stream (see Section 6.2.1) by each peer, and it MUST NOT
   be sent subsequently.  If an endpoint receives a second SETTINGS
   frame on the control stream, the endpoint MUST respond with a
   connection error of type H3_FRAME_UNEXPECTED.

   SETTINGS frames MUST NOT be se

[RFC 9113 §6.5.1]
§6.5.1 SETTINGS Format

The frame payload of a SETTINGS frame consists of zero or more
   settings, each consisting of an unsigned 16-bit setting identifier
   and an unsigned 32-bit value.

   SETTINGS Frame {
     Length (24),
     Type (8) = 0x04,

     Unused Flags (7),
     ACK Flag (1),

     Reserved (1),
     Stream Identifier (31) = 0,

     Setting (48) ...,
   }

   Setting {
     Identifier (16),
     Value (32),
   }

                      Figure 7: SETTINGS Frame Format

   The Length, Type, Unused Flag(s), Reserved, and Stream Identifier
   fields are described in Section 4.  The frame payload of a SETTINGS
   frame contains any number of Setting fields, each of which consists
   of:

   Identifier:  A 16-bit setting identifier; see Section 6.5.2.

   Value:  A 32-bit value for the setting.

[RFC 9114 §12.2]
§12.2 Informative References

hat HTTP/2 specifies via the SETTINGS
   frame are superseded by QUIC transport parameters in HTTP/3.  The
   HTTP-level setting that is retained in HTTP/3 has the same value as
   in HTTP/2.  The superseded settings are reserved, and their receipt
   is an error.  See Section 7.2.4.1 for discussion of both the retained
   and reserved values.

   Below is a listing of how each HTTP/2 SETTINGS parameter is mapped:

   SETTINGS_HEADER_TABLE_SIZE (0x01):  See [QPACK].

   SETTINGS_ENABLE_PUSH (0x02):  This is removed in favor of the
      MAX_PUSH_ID frame, which provides a more granular control over
      server push.  Specifying a setting with the identifier 0x02
      (corresponding to the SETTINGS_ENABLE_PUSH parameter) in the
      HTTP/3 SETTINGS frame is an error.

   SETTINGS_MAX_CON

[RFC 9114 §12.2]
§12.2 Informative References

ned by extensions to HTTP/2 need to be separately
   registered for HTTP/3 if still applicable.  The IDs of frames defined
   in [HTTP/2] have been reserved for simplicity.  Note that the frame
   type space in HTTP/3 is substantially larger (62 bits versus 8 bits),
   so many HTTP/3 frame types have no equivalent HTTP/2 code points.
   See Section 11.2.1.

A.3.  HTTP/2 SETTINGS Parameters

   An important difference from HTTP/
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 0.8

---

## q018 (identifier_lookup)

**Pergunta:** What frame type value identifies a DATA frame in HTTP/3?

**Resposta gerada:** 0x00 (RFC 9114 §7.2)

**Gabarito:** Type=0x00.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9114 §7.1]
§7.1 Frame Layout

All frames have the following format:

   HTTP/3 Frame Format {
     Type (i),
     Length (i),
     Frame Payload (..),
   }

                       Figure 3: HTTP/3 Frame Format

   A frame includes the following fields:

   Type:  A variable-length integer that identifies the frame type.

   Length:  A variable-length integer that describes the length in bytes
      of the Frame Payload.

   Frame Payload:  A payload, the semantics of which are determined by
      the Type field.

   Each frame's payload MUST contain exactly the fields identified in
   its description.  A frame payload that contains additional bytes
   after the identified fields or a frame payload that terminates before
   the end of the identified fields MUST be treated as a connection
   error of type H3_FRAME_ERROR.

[RFC 9114 §7.2 / RFC 9114 §7.2.1]
§7.2.1 DATA

DATA frames (type=0x00) convey arbitrary, variable-length sequences
   of bytes associated with HTTP request or response content.

   DATA frames MUST be associated with an HTTP request or response.  If
   a DATA frame is received on a control stream, the recipient MUST
   respond with a connection error of type H3_FRAME_UNEXPECTED.

   DATA Frame {
     Type (i) = 0x00,
     Length (i),
     Data (..),
   }

                            Figure 4: DATA Frame

[RFC 9113 §4 / RFC 9113 §4.1]
§4.1 Frame Format

Once the HTTP/2 connection is established, endpoints can begin
   exchanging frames.All frames begin with a fixed 9-octet header followed by a variable-
   length frame payload.

   HTTP Frame {
     Length (24),
     Type (8),

     Flags (8),

     Reserved (1),
     Stream Identifier (31),

     Frame Payload (..),
   }

                           Figure 1: Frame Layout

   The fields of the frame header are defined as:

   Length:  The length of the frame payload expressed as an unsigned
      24-bit integer in units of octets.  Values greater than 2^14
      (16,384) MUST NOT be sent unless the receiver has set a larger
      value for SETTINGS_MAX_FRAME_SIZE.

      The 9 octets of the frame header are not included in this value.

   Type:  The 8-bit type of the frame.  The frame type determines the
      format and semantics of the frame.  Frames defined in this
  

[RFC 9113 §6.7]
§6.7 PING

The PING frame (type=0x06) is a mechanism for measuring a minimal
   round-trip time from the sender, as well as determining whether an
   idle connection is still functional.  PING frames can be sent from
   any endpoint.

   PING Frame {
     Length (24) = 0x08,
     Type (8) = 0x06,

     Unused Flags (7),
     ACK Flag (1),

     Reserved (1),
     Stream Identifier (31) = 0,

     Opaque Data (64),
   }

                        Figure 9: PING Frame Format

   The Length, Type, Unused Flag(s), Reserved, and Stream Identifier
   fields are described in Section 4.

   In addition to the frame header, PING frames MUST contain 8 octets of
   opaque data in the frame payload.  A send
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q028 (identifier_lookup)

**Pergunta:** What frame type value identifies a GOAWAY frame in HTTP/2?

**Resposta gerada:** 0x07 (RFC 9113 §6.8)

**Gabarito:** Type=0x07.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9114 §7.2.6]
§7.2.6 GOAWAY

or a client-
   initiated bidirectional stream encoded as a variable-length integer.
   A client MUST treat receipt of a GOAWAY frame containing a stream ID
   of any other type as a connection error of type H3_ID_ERROR.

   In the client-to-server direction, the GOAWAY frame carries a push ID
   encoded as a variable-length integer.

   The GOAWAY frame applies to the entire connection, not a specific
   stream.  A client MUST treat a GOAWAY frame on a stream other than
   the control stream as a connection error of type H3_FRAME_UNEXPECTED.

   See Section 5.2 for more information on the use of the GOAWAY frame.

[RFC 9114 §7.2.6]
§7.2.6 GOAWAY

The GOAWAY frame (type=0x07) is used to initiate graceful shutdown of
   an HTTP/3 connection by either endpoint.  GOAWAY allows an endpoint
   to stop accepting new requests or pushes while still finishing
   processing of previously received requests and pushes.  This enables
   administrative actions, like server maintenance.  GOAWAY by itself
   does not close a connection.

   GOAWAY Frame {
     Type (i) = 0x07,
     Length (i),
     Stream ID/Push ID (i),
   }

                           Figure 9: GOAWAY Frame

   The GOAWAY frame is always sent on the control stream.  In the
   server-to-client direction, it carries a QUIC stream ID for a client-
   initiated bidirectional stream encoded as a variable-length integer.
   A client MUST treat receipt of a GOAWAY frame containing a str

[RFC 9114 §7.1]
§7.1 Frame Layout

All frames have the following format:

   HTTP/3 Frame Format {
     Type (i),
     Length (i),
     Frame Payload (..),
   }

                       Figure 3: HTTP/3 Frame Format

   A frame includes the following fields:

   Type:  A variable-length integer that identifies the frame type.

   Length:  A variable-length integer that describes the length in bytes
      of the Frame Payload.

   Frame Payload:  A payload, the semantics of which are determined by
      the Type field.

   Each frame's payload MUST contain exactly the fields identified in
   its description.  A frame payload that contains additional bytes
   after the identified fields or a frame payload that terminates before
   the end of the identified fields MUST be treated as a connection
   error of type H3_FRAME_ERROR.

[RFC 9113 §4 / RFC 9113 §4.1]
§4.1 Frame Format

Once the HTTP/2 connection is established, endpoints can begin
   exchanging frames.All frames begin with a fixed 9-octet header followed by a variable-
   length frame payload.

   HTTP Frame {
     Length (24),
     Type (8),

     Flags (8),

     Reserved (1),
     Stream Identifier (31),

     Frame Payload (..),
   }

                           Figure 1: Frame Layout

   The fields of the frame header are defined as:

   Length:  The length of the frame payload expressed as an unsigned
      24-bit integer in units of octets.  Values greater than 2^14
      (16,384) MUST NOT be sent unless the receiver has set
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q030 (identifier_lookup)

**Pergunta:** What error code value indicates QPACK_DECOMPRESSION_FAILED?

**Resposta gerada:** 0x0200 (RFC 9204 §6)

**Gabarito:** 0x0200.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9204 §6]
§6 Error Handling

The following error codes are defined for HTTP/3 to indicate failures
   of QPACK that prevent the stream or connection from continuing:

   QPACK_DECOMPRESSION_FAILED (0x0200):  The decoder failed to interpret
      an encoded field section and is not able to continue decoding that
      field section.

   QPACK_ENCODER_STREAM_ERROR (0x0201):  The decoder failed to interpret
      an encoder instruction received on the encoder stream.

   QPACK_DECODER_STREAM_ERROR (0x0202):  The encoder failed to interpret
      a decoder instruction received on the decoder stream.

[RFC 9204 §2.2.1]
§2.2.1 Blocked Decoding


   greater than or equal to the Required Insert Count for all encoded
   field sections the decoder has started reading from the stream.

   When processing encoded field sections, the decoder expects the
   Required Insert Count to equal the lowest possible value for the
   Insert Count with which the field section can be decoded, as
   prescribed in Section 2.1.2.  If it encounters a Required Insert
   Count smaller than expected, it MUST treat this as a connection error
   of type QPACK_DECOMPRESSION_FAILED; see Section 2.2.3.  If it
   encounters a Required Insert Count larger than expected, it MAY treat
   this as a connection error of type QPACK_DECOMPRESSION_FAILED.

[RFC 9204 §8.3]
§8.3 Error Code Registration

This document specifies three error codes.  The entries in the
   following table are registered in the "HTTP/3 Error Codes" registry
   established in [HTTP/3].

   +============================+========+=============+===============+
   | Name                       | Code   |Description  | Specification |
   +============================+========+=============+===============+
   | QPACK_DECOMPRESSION_FAILED | 0x0200 |Decoding of a| Section 6     |
   |                            |        |field section|               |
   |                            |        |failed       |               |
   +----------------------------+--------+-------------+---------------+
   | QPACK_ENCODER_STREAM_ERROR | 0x0201 |Error on the | Section 6     |
   |                            |        |encoder    

[RFC 9204 §2.2.3]
§2.2.3 Invalid References

If the decoder encounters a reference in a field line representation
   to a dynamic table entry that has already been evicted or that has an
   absolute index greater than or equal to the declared Required Insert
   Count (Section 4.5.1), it MUST treat this as a connection error of
   type QPACK_DECOMPRESSION_FAILED.

   If the decoder encounters a reference in an encoder instruction to a
   dynamic table entry that has already been evicted, it MUST treat this
   as a connection error of type QPACK_ENCODER_STREAM_ERROR.

[RFC 9204 §7.4]
§7.4 Implementation Limits

An implementation of QPACK needs to ensure that large values for
   integers, long encoding for integers, or long string literals do not
   create security weaknesses.

   An implementation has to set
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q019 (multi_section)

**Pergunta:** How does the meaning of the max-age directive differ depending on whether it appears in a request or a response?

**Resposta gerada:** When the max-age directive appears in a request, it indicates that the client prefers a response whose age is less than or equal to the specified number of seconds, and unless the max-stale request directive is also present, the client does not wish to receive a stale response (RFC 9111 §5.2.1.1).

When the max-age directive appears in a response, it indicates that the response is to be considered stale after its age is greater than the specified number of seconds (RFC 9111 §5.2.2.1).

**Gabarito:** As a request directive, max-age says the client wants a response no older than the given number of seconds. As a response directive, max-age says the response should be considered stale once it is older than that.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9111 §5.2.1.1]
§5.2.1.1 max-age

Argument syntax:

      delta-seconds (see Section 1.2.2)

   The max-age request directive indicates that the client prefers a
   response whose age is less than or equal to the specified number of
   seconds.  Unless the max-stale request directive is also present, the
   client does not wish to receive a stale response.

   This directive uses the token form of the argument syntax: e.g.,
   'max-age=5' not 'max-age="5"'.  A sender MUST NOT generate the
   quoted-string form.

[RFC 9111 §5.2.2.1]
§5.2.2.1 max-age

Argument syntax:

      delta-seconds (see Section 1.2.2)

   The max-age response directive indicates that the response is to be
   considered stale after its age is greater than the specified number
   of seconds.

   This directive uses the token form of the argument syntax: e.g.,
   'max-age=5' not 'max-age="5"'.  A sender MUST NOT generate the
   quoted-string form.

[RFC 9111 §5.2.2.10]
§5.2.2.10 s-maxage

Argument syntax:

      delta-seconds (see Section 1.2.2)

   The s-maxage response directive indicates that, for a shared cache,
   the maximum age specified by this directive overrides the maximum age
   specified by either the max-age directive or the Expires header
   field.

   The s-maxage directive incorporates the semantics of the
   proxy-revalidate response directive (Section 5.2.2.8) for a shared
   cache.  A shared cache MUST NOT reuse a stale response with s-maxage
   to satisfy another request until it has been successfully validated
   by the origin, as defined by Section 4.3.  This directive also
   permits a shared cache to reuse a response to a request containing an
   Authorization header field, subject to the above requirements on
   maximum age and revalidation (Section 3.5).

   This directive uses the token form of the argument syntax: e.g.,
   's-maxage=10' not 's-maxage="10"'.  A sender MUST NOT generate the
   quoted-string form.

[RFC 9111 §5.2.1.2]
§5.2.1.2 max-stale

Argument syntax:

      delta-seconds (see Section 1.2.2)

   The max-stale request directive indicates that the client will accept
   a response that has exceeded its freshness lifetime.  If a value is
   present, then the client is willing to accept a response that has
   exceeded its freshness lifetime by no more than the specified number
   of seconds.  If no value is assigned to max-stale, then the client
   will accept a stale response of any age.

   This directive uses the token form of the argument syntax: e.g.,
   'max-stale=10' not 'max-stale="10"'.  A sender MUST NOT generate the
   quoted-string form.

[RFC 9111 §5.2]
§5.2 Cache-Control

The "Cache-Control" header field is used to list directives for
   caches along the request/response chain.  Cache directives are
   unidirectional, in that the presence of a directive in a request does
   not imply that the same directive is present or copied in the
   response.

   See Section 5.2.3 for information about how Cache-Control directives

```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q021 (multi_section)

**Pergunta:** Under what condition can a client safely retry a request automatically after a connection closes, and which methods satisfy it by default?

**Resposta gerada:** A client can safely retry a request automatically after a connection closes if the request has an idempotent method. Idempotent methods include GET, PUT, and DELETE. 

RFC 9110 §9.2.2

**Gabarito:** A request can be safely retried automatically if its method is idempotent - repeating it has the same effect as sending it once. PUT, DELETE and the safe methods are idempotent by default.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9110 §9.2.2]
§9.2.2 Idempotent Methods

ier approach and attempt to guess when an
   automatic retry is possible.  For example, a client might
   automatically retry a POST request if the underlying transport
   connection closed before any part of a response is received,
   particularly if an idle persistent connection was used.

   A proxy MUST NOT automatically retry non-idempotent requests.  A
   client SHOULD NOT automatically retry a failed automatic retry.

[RFC 9112 §9.3.1]
§9.3.1 Retrying Requests

Connections can be closed at any time, with or without intention.
   Implementations ought to anticipate the need to recover from
   asynchronous close events.  The conditions under which a client can
   automatically retry a sequence of outstanding requests are defined in
   Section 9.2.2 of [HTTP].

[RFC 9110 §9.2.2]
§9.2.2 Idempotent Methods

   repeated automatically if a communication failure occurs before the
   client is able to read the server's response.  For example, if a
   client sends a PUT request and the underlying connection is closed
   before any response is received, then the client can establish a new
   connection and retry the idempotent request.  It knows that repeating
   the request will have the same intended effect, even if the original
   request succeeded, though the response might differ.

   A client SHOULD NOT automatically retry a request with a non-
   idempotent method unless it has some means to know that the request
   semantics are actually idempotent, regardless of the method, or some
   means to detect that the original request was never applied.

   For example, a user agent can repeat a PO

[RFC 9114 §4.1.1]
§4.1.1 Request Cancellation and Rejection

MAY ignore the cancellation and use the response.  However, if
   a stream is cancelled after receiving a partial response, the
   response SHOULD NOT be used.  Only idempotent actions such as GET,
   PUT, or DELETE can be safely retried; a client SHOULD NOT
   automatically retry a request with a non-idempotent method unless it
   has some means to know that the request semantics are idempotent
   independent of the method or some means to detect that the original
   request was never applied.  See Section 9.2.2 of [HTTP] for more
   details.

[RFC 9112 §9.3.2]
§9.3.2 Pipelining

A client that supports persistent connections MAY "pipeline" its
   requests (i.e., send multiple requests without waiting for each
   response).  A server MAY process a sequence of pipelined requests in
   parallel if they all have safe methods (Section 9.2.1 of [HTTP]), but
   it MUST send the corresponding responses in the same order that the
   requests were received.

   A client that pipelines requests SHOULD retry unanswered requests if
   the connection closes before it receives all of the corresponding
   responses.  When retrying pipelined requests after a failed
   connection (a connection not explicitly closed by the server in its
   last complete response), a cl
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q023 (multi_section)

**Pergunta:** How is the size of an entry in HPACK's dynamic table calculated, given that the dynamic table indexes header fields?

**Resposta gerada:** The size of an entry in HPACK's dynamic table is calculated as the sum of its name's length in octets, its value's length in octets, and 32. RFC 7541 §4.1

**Gabarito:** The dynamic table (introduced alongside the static table for indexing header fields) holds entries whose size is the sum of the name's length in octets, the value's length in octets, and 32 additional octets - calculated on the unencoded name and value, without any Huffman encoding applied.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9204 §3.2.1]
§3.2.1 Dynamic Table Size

The size of the dynamic table is the sum of the size of its entries.

   The size of an entry is the sum of its name's length in bytes, its
   value's length in bytes, and 32 additional bytes.  The size of an
   entry is calculated using the length of its name and value without
   Huffman encoding applied.

[RFC 7541 §4 / RFC 7541 §4.1]
§4.1 Calculating Table Size

To limit the memory requirements on the decoder side, the dynamic
   table is constrained in size.The size of the dynamic table is the sum of the size of its entries.

   The size of an entry is the sum of its name's length in octets (as
   defined in Section 5.2), its value's length in octets, and 32.

   The size of an entry is calculated using the length of its name and
   value without any Huffman encoding applied.

      Note: The additional 32 octets account for an estimated overhead
      associated with an entry.  For example, an entry structure using
      two 64-bit pointers to reference the name and the value of the
      entry and two 64-bit integers for counting the number of
      references to the name and value would have 32 octets of overhead.

[RFC 7541 §2.3.2]
§2.3.2 Dynamic Table

The dynamic table consists of a list of header fields maintained in
   first-in, first-out order.  The first and newest entry in a dynamic
   table is at the lowest index, and the oldest entry of a dynamic table
   is at the highest index.






   The dynamic table is initially empty.  Entries are added as each
   header block is decompressed.

   The dynamic table can contain duplicate entries (i.e., entries with
   the same name and same value).  Therefore, duplicate entries MUST NOT
   be treated as an error by a decoder.

   The encoder decides how to update the dynamic table and as such can
   control how much memory is used by the dynamic table.  To limit the
   memory requirements of the decoder, the dynamic table size is
   strictly bounded (see Section 4.2).

   The decoder updates the dynamic table during the processing of a list
   of header field representations (see Section 3.2).

[RFC 7541 §2.3]
§2.3 Indexing Tables

HPACK uses two tables for associating header fields to indexes.  The
   static table (see Section 2.3.1) is predefined and contains common
   header fields (most of them with an empty value).  The dynamic table
   (see Section 2.3.2) is dynamic and can be used by the encoder to
   index header fields repeated in the encoded header lists.

   These two tables are combined into a single address space for
   defining index values (see Section 2.3.3).

[RFC 9113 §4.3.1]
§4.3.1 Compression State

initial value of the SETTINGS_HEADER_TABLE_SIZE setting.

   Any change to the maximum value set using SETTINGS_HEADER_TABLE_SIZE
   takes effect when the endpoint acknowledges settings (Section 6.5.3).
   The HPACK encoder at that endpoint can set the dynamic table to any
   size up to the maximum value set by the decoder.  An HP
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q026 (multi_section)

**Pergunta:** 400 Bad Request and 404 Not Found are both client-error status codes - what is the actual difference in what each one tells the client?

**Resposta gerada:** According to RFC 9110 §15.5.1, a 400 (Bad Request) status code indicates that the server cannot or will not process the request due to something that is perceived to be a client error, such as malformed request syntax, invalid request message framing, or deceptive request routing.

According to RFC 9110 §15.5.5, a 404 (Not Found) status code indicates that the origin server did not find a current representation for the target resource or is not willing to disclose that one exists.

The key difference between the two is that 400 indicates a problem with the request itself, while 404 indicates that the requested resource does not exist.

**Gabarito:** 400 means the server perceives an error in the request itself (malformed syntax, invalid framing, deceptive routing). 404 means the request was understood but the origin server found no current representation for the target resource, or won't disclose that one exists.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9110 §15.5.1]
§15.5.1 400 Bad Request

The 400 (Bad Request) status code indicates that the server cannot or
   will not process the request due to something that is perceived to be
   a client error (e.g., malformed request syntax, invalid request
   message framing, or deceptive request routing).

[RFC 9110 §15.5.5]
§15.5.5 404 Not Found

The 404 (Not Found) status code indicates that the origin server did
   not find a current representation for the target resource or is not
   willing to disclose that one exists.  A 404 status code does not
   indicate whether this lack of representation is temporary or
   permanent; the 410 (Gone) status code is preferred over 404 if the
   origin server knows, presumably through some configurable means, that
   the condition is likely to be permanent.

   A 404 response is heuristically cacheable; i.e., unless otherwise
   indicated by the method definition or explicit cache controls (see
   Section 4.2.2 of [CACHING]).

[RFC 9110 §15]
§15 Status Codes

The status code of a response is a three-digit integer code that
   describes the result of the request and the semantics of the
   response, including whether the request was successful and what
   content is enclosed (if any).  All valid status codes are within the
   range of 100 to 599, inclusive.

   The first digit of the status code defines the class of response.
   The last two digits do not have any categorization role.  There are
   five values for the first digit:

   *  1xx (Informational): The request was received, continuing process

   *  2xx (Successful): The request was successfully received,
      understood, and accepted

   *  3xx (Redirection): Further action needs to be taken in order to
      complete the request

   *  4xx (Client Error): The request contains bad sy

[RFC 9110 §15]
§15 Status Codes

  *  3xx (Redirection): Further action needs to be taken in order to
      complete the request

   *  4xx (Client Error): The request contains bad syntax or cannot be
      fulfilled

   *  5xx (Server Error): The server failed to fulfill an apparently
      valid request

   HTTP status codes are extensible.  A client is not required to
   understand the meaning of all registered status codes, though such
   understanding is obviously desirable.  However, a client MUST
   understand the class of any status code, as indicated by the first
   digit, and treat an unrecognized status code as being equivalent to
   the x00 status code of that class.

   For example, if a client receives an unrecognized status code of 471,
   it can see from the first digit that there was something wrong with


[RFC 9112 §6.3]
§6.3 Message Body Length

the message is processed with that single value used as the
       Content-Length field value).  If the unrecoverable error is in a
       request message, the server MUST respond with a 400 (Bad Request)
       status code and then close the connection.  If it is in a
       response message received by a 
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q032 (superseded)

**Pergunta:** What does the GOAWAY frame allow an HTTP/2 endpoint to do?

**Resposta gerada:** The GOAWAY frame allows an endpoint to stop accepting new requests or pushes while still finishing processing of previously received requests and pushes.

**Gabarito:** Initiate shutdown of a connection (or signal a serious error condition), gracefully stopping acceptance of new streams while finishing in-flight ones.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9114 §7.2.6]
§7.2.6 GOAWAY

The GOAWAY frame (type=0x07) is used to initiate graceful shutdown of
   an HTTP/3 connection by either endpoint.  GOAWAY allows an endpoint
   to stop accepting new requests or pushes while still finishing
   processing of previously received requests and pushes.  This enables
   administrative actions, like server maintenance.  GOAWAY by itself
   does not close a connection.

   GOAWAY Frame {
     Type (i) = 0x07,
     Length (i),
     Stream ID/Push ID (i),
   }

                           Figure 9: GOAWAY Frame

   The GOAWAY frame is always sent on the control stream.  In the
   server-to-client direction, it carries a QUIC stream ID for a client-
   initiated bidirectional stream encoded as a variable-length integer.
   A client MUST treat receipt of a GOAWAY frame containing a str

[RFC 9114 §12.2]
§12.2 Informative References

rences the PUSH_PROMISE frame
      using a push ID.  See Section 7.2.5.

   PING (0x06):  PING frames do not exist in HTTP/3, as QUIC provides
      equivalent functionality.

   GOAWAY (0x07):  GOAWAY does not contain an error code.  In the
      client-to-server direction, it carries a push ID instead of a
      server-initiated stream ID.  See Section 7.2.6.

   WINDOW_UPDATE (0x08):  WINDOW_UPDATE frames do not exist in HTTP/3,
      since QUIC provides flow control.

   CONTINUATION (0x09):  CONTINUATION frames do not exist in HTTP/3;
      instead, larger HEADERS/PUSH_PROMISE frames than HTTP/2 are
      permitted.

   Frame types defined by extensions to HTTP/2 need to be separately
   registered for HTTP/3 if still applicable.  The IDs of frames defined
   in [HTTP/2] have been re

[RFC 9113 §6.8]
§6.8 GOAWAY

he receiver of the GOAWAY
   frame can treat the streams as though they had never been created at
   all, thereby allowing those streams to be retried later on a new
   connection.

   Endpoints SHOULD always send a GOAWAY frame before closing a
   connection so that the remote peer can know whether a stream has been
   partially processed or not.  For example, if an HTTP client sends a
   POST at the same time that a server closes a connection, the client
   cannot know if the server started to process that POST request if the
   server does not send a GOAWAY frame to indicate what streams it might
   have acted on.

   An endpoint might choose to close a connection without sending a
   GOAWAY for misbehaving peers.

   A GOAWAY frame might not immediately precede closing of the
   connec

[RFC 9114 §5.2]
§5.2 Connection Shutdown

no requests or pushes were processed.

   The information in the GOAWAY frame enables a client and server to
   agree on which requests or pushes were accepted prior to the shutdown
   of the HTTP/3 connection.  Upon sending a GOAWAY frame, the endpoint
   SHOULD explicitly cancel (see Sections 4.1.1 and 7.2.3) any requests
   or pushes that have identifiers greater than or equal to the one
   indicated, in order to clean up transport stat
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q034 (superseded)

**Pergunta:** How does chunked transfer coding structure the body of a message?

**Resposta gerada:** The chunked transfer coding structures the body of a message as a series of chunks, each with its own size indicator, followed by an OPTIONAL trailer section containing trailer fields. The structure is as follows:

chunked-body = *chunk last-chunk trailer-section CRLF

chunk = chunk-size [ chunk-ext ] CRLF chunk-data CRLF
chunk-size = 1*HEXDIG
last-chunk = 1*("0") [ chunk-ext ] CRLF
chunk-data = 1*OCTET; a sequence of chunk-size octets

RFC 9112 §7.1

**Gabarito:** As a series of chunks, each with its own size indicator, optionally followed by a trailer section.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9112 §6.1]
§6.1 Transfer-Encoding

nked is applied to a request's content,
   the sender MUST apply chunked as the final transfer coding to ensure
   that the message is properly framed.  If any transfer coding other
   than chunked is applied to a response's content, the sender MUST
   either apply chunked as the final transfer coding or terminate the
   message by closing the connection.

   For example,

   Transfer-Encoding: gzip, chunked

   indicates that the content has been compressed using the gzip coding
   and then chunked using the chunked coding while forming the message
   body.

   Unlike Content-Encoding (Section 8.4.1 of [HTTP]), Transfer-Encoding
   is a property of the message, not of the representation.  Any
   recipient along the request/response chain MAY decode the received
   transfer coding(s) or ap

[RFC 9112 §6.1]
§6.1 Transfer-Encoding

   In HTTP's case, Transfer-Encoding is primarily intended to accurately
   delimit dynamically generated content.  It also serves to distinguish
   encodings that are only applied in transit from the encodings that
   are a characteristic of the selected representation.

   A recipient MUST be able to parse the chunked transfer coding
   (Section 7.1) because it plays a crucial role in framing messages
   when the content size is not known in advance.  A sender MUST NOT
   apply the chunked transfer coding more than once to a message body
   (i.e., chunking an already chunked message is not allowed).  If any
   transfer coding other than chunked is applied to a request's content,
   the sender MUST apply chunked as the final transfer coding to ensure
   that the message is properly framed

[RFC 9112 §6.3]
§6.3 Message Body Length

e
       message downstream.

   4.  If a Transfer-Encoding header field is present and the chunked
       transfer coding (Section 7.1) is the final encoding, the message
       body length is determined by reading and decoding the chunked
       data until the transfer coding indicates the data is complete.

       If a Transfer-Encoding header field is present in a response and
       the chunked transfer coding is not the final encoding, the
       message body length is determined by reading the connection until
       it is closed by the server.

       If a Transfer-Encoding header field is present in a request and
       the chunked transfer coding is not the final encoding, the
       message body length cannot be determined reliably; the server
       MUST respond with the 400 (B

[RFC 9112 §7.1]
§7.1 Chunked Transfer Coding

The chunked transfer coding wraps content in order to transfer it as
   a series of chunks, each with its own size indicator, followed by an
   OPTIONAL trailer section containing trailer fields.  Chunked enables
   content streams of unknown size to be transferred as a sequence of
   length-delimited buffers, which enables the sender to retain
   connection persistence and the recipient to know when it has received
   the
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q036 (superseded)

**Pergunta:** What header field tells a client how long to wait before retrying, and what two formats can its value take?

**Resposta gerada:** The "Retry-After" header field tells a client how long to wait before retrying. Its value can be either an HTTP-date or a number of seconds to delay after receiving the response. 

RFC 9110 §10.2.3

**Gabarito:** Retry-After. Its value is either an HTTP-date or a number of delay-seconds.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9110 §10.2.3]
§10.2.3 Retry-After

Servers send the "Retry-After" header field to indicate how long the
   user agent ought to wait before making a follow-up request.  When
   sent with a 503 (Service Unavailable) response, Retry-After indicates
   how long the service is expected to be unavailable to the client.
   When sent with any 3xx (Redirection) response, Retry-After indicates
   the minimum time that the user agent is asked to wait before issuing
   the redirected request.

   The Retry-After field value can be either an HTTP-date or a number of
   seconds to delay after receiving the response.

     Retry-After = HTTP-date / delay-seconds

   A delay-seconds value is a non-negative decimal integer, representing
   time in seconds.

     delay-seconds  = 1*DIGIT

   Two examples of its use are

   Retry-After: Fri, 31 Dec 1999 23:59:59 GMT
   Retry-After: 120

   In the latter example, the delay is 2 minutes.

[RFC 9110 §16.1.2]
§16.1.2 Considerations for New Methods

mpotent (Section 9.2.2), cacheable
   (Section 9.2.3), what semantics are to be associated with the request
   content (if any), and what refinements the method makes to header
   field or status code semantics.  If the new method is cacheable, its
   definition ought to describe how, and under what conditions, a cache
   can store a response and use it to satisfy a subsequent request.  The
   new method ought to describe whether it can be made conditional
   (Section 13.1) and, if so, how a server responds when the condition
   is false.  Likewise, if the new method might have some use for
   partial response semantics (Section 14.2), it ought to document this,
   too.

      |  *Note:* Avoid defining a method name that starts with "M-",
      |  since that prefix might be misinterpreted 

[RFC 9111 §5.2.3]
§5.2.3 Extension Directives

: private, community="UCI"

   A cache that recognizes such a community cache directive could
   broaden its behavior in accordance with that extension.  A cache that
   does not recognize the community cache directive would ignore it and
   adhere to the private directive.

   New extension directives ought to consider defining:

   *  What it means for a directive to be specified multiple times,

   *  When the directive does not take an argument, what it means when
      an argument is present,

   *  When the directive requires an argument, what it means when it is
      missing, and

   *  Whether the directive is specific to requests, specific to
      responses, or able to be used in either.

[RFC 9110 §5.3]
§5.3 Field Order

mentations can decide when not to handle a message as early as
   possible.

   A server MUST NOT apply a request to the target resource until it
   receives the entire request header section, since later header field
   lines might include conditionals, authentication credentials, or
   deliberately misleading duplicate header fields that could impact
   request processing.

[RFC 9110 §16.3.2.2]
§16.3.2.2 Co
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q037 (explicit_historical_version)

**Pergunta:** In RFC 7540, what does the GOAWAY frame allow an HTTP/2 endpoint to do?

**Resposta gerada:** Initiate shutdown of a connection or to signal serious error conditions. GOAWAY allows an endpoint to gracefully stop accepting new streams while still finishing processing of previously established streams. This enables administrative actions, like server maintenance. 

RFC 7540 §6.8

**Gabarito:** Initiate shutdown of a connection (or signal a serious error condition), gracefully stopping acceptance of new streams while finishing in-flight ones.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9114 §7.2.6]
§7.2.6 GOAWAY

The GOAWAY frame (type=0x07) is used to initiate graceful shutdown of
   an HTTP/3 connection by either endpoint.  GOAWAY allows an endpoint
   to stop accepting new requests or pushes while still finishing
   processing of previously received requests and pushes.  This enables
   administrative actions, like server maintenance.  GOAWAY by itself
   does not close a connection.

   GOAWAY Frame {
     Type (i) = 0x07,
     Length (i),
     Stream ID/Push ID (i),
   }

                           Figure 9: GOAWAY Frame

   The GOAWAY frame is always sent on the control stream.  In the
   server-to-client direction, it carries a QUIC stream ID for a client-
   initiated bidirectional stream encoded as a variable-length integer.
   A client MUST treat receipt of a GOAWAY frame containing a str

[RFC 7540 §6.8 [OBSOLETED - see RFC 9113 instead]]
§6.8 GOAWAY

   Additional Debug Data (*)                    |
    +---------------------------------------------------------------+

                     Figure 13: GOAWAY Payload Format

   The GOAWAY frame does not define any flags.

   The GOAWAY frame applies to the connection, not a specific stream.
   An endpoint MUST treat a GOAWAY frame with a stream identifier other
   than 0x0 as a connection error (Section 5.4.1) of type
   PROTOCOL_ERROR.

   The last stream identifier in the GOAWAY frame contains the highest-
   numbered stream identifier for which the sender of the GOAWAY frame
   might have taken some action on or might yet take action on.  All
   streams up to and including the identified stream might have been
   processed in some way.  The last stream identifier can be set to 0 if
  

[RFC 9114 §12.2]
§12.2 Informative References

rences the PUSH_PROMISE frame
      using a push ID.  See Section 7.2.5.

   PING (0x06):  PING frames do not exist in HTTP/3, as QUIC provides
      equivalent functionality.

   GOAWAY (0x07):  GOAWAY does not contain an error code.  In the
      client-to-server direction, it carries a push ID instead of a
      server-initiated stream ID.  See Section 7.2.6.

   WINDOW_UPDATE (0x08):  WINDOW_UPDATE frames do not exist in HTTP/3,
      since QUIC provides flow control.

   CONTINUATION (0x09):  CONTINUATION frames do not exist in HTTP/3;
      instead, larger HEADERS/PUSH_PROMISE frames than HTTP/2 are
      permitted.

   Frame types defined by extensions to HTTP/2 need to be separately
   registered for HTTP/3 if still applicable.  The IDs of frames defined
   in [HTTP/2] have been re

[RFC 9114 §5.2]
§5.2 Connection Shutdown

no requests or pushes were processed.

   The information in the GOAWAY frame enables a client and server to
   agree on which requests or pushes were accepted prior to the shutdown
   of the HTTP/3 connection.  Upon sending a GOAWAY frame, the endpoint
   SHOULD explicitly cancel (see Sections 4.1.1 and 7.2.3) any requests
   or pushes that have identifiers greater than or equal to the one
   indicated, 
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

## q040 (explicit_historical_version)

**Pergunta:** In RFC 2616, what does the Last-Modified header field indicate, and what format is its value?

**Resposta gerada:** The Last-Modified entity-header field indicates the date and time at which the origin server believes the variant was last modified. The value of the Last-Modified header field is in the format of an HTTP-date. 

RFC 2616 §14.29

**Gabarito:** The date and time at which the origin server believes the variant was last modified. Its value is an HTTP-date.

**CORRECTNESS - TEU_VEREDICTO:** [correct | partially_correct | incorrect] -> correct

<details><summary>Contexto fornecido (para faithfulness)</summary>

```
[RFC 9110 §8.8.2]
§8.8.2 Last-Modified

The "Last-Modified" header field in a response provides a timestamp
   indicating the date and time at which the origin server believes the
   selected representation was last modified, as determined at the
   conclusion of handling the request.

     Last-Modified = HTTP-date

   An example of its use is

   Last-Modified: Tue, 15 Nov 1994 12:45:26 GMT

[RFC 2616 §14.29 [OBSOLETED - see RFC 7230, RFC 7231, RFC 7232, RFC 7233, RFC 7234, RFC 7235 instead]]
§14.29 Last-Modified

The Last-Modified entity-header field indicates the date and time at
   which the origin server believes the variant was last modified.

       Last-Modified  = "Last-Modified" ":" HTTP-date






   An example of its use is

       Last-Modified: Tue, 15 Nov 1994 12:45:26 GMT

   The exact meaning of this header field depends on the implementation
   of the origin server and the nature of the original resource. For
   files, it may be just the file system last-modified time. For
   entities with dynamically included parts, it may be the most recent
   of the set of last-modify times for its component parts. For database
   gateways, it may be the last-update time stamp of the record. For
   virtual objects, it may be the last time the internal state changed.

   An origin server MUST NOT 

[RFC 2616 §3.5 [OBSOLETED - see RFC 7230, RFC 7231, RFC 7232, RFC 7233, RFC 7234, RFC 7235 instead]]
§3.5 Content Codings

value
   describes the content-coding, what is more important is that it
   indicates what decoding mechanism will be required to remove the
   encoding.

   The Internet Assigned Numbers Authority (IANA) acts as a registry for
   content-coding value tokens. Initially, the registry contains the
   following tokens:

   gzip An encoding format produced by the file compression program
        "gzip" (GNU zip) as described in RFC 1952 [25]. This format is a
        Lempel-Ziv coding (LZ77) with a 32 bit CRC.

   compress
        The encoding format produced by the common UNIX file compression
        program "compress". This format is an adaptive Lempel-Ziv-Welch
        coding (LZW).

        Use of program names for the identification of encoding formats
        is not desirable and is dis

[RFC 2616 §14.35.2 [OBSOLETED - see RFC 7230, RFC 7231, RFC 7232, RFC 7233, RFC 7234, RFC 7235 instead]]
§14.35.2 Range Retrieval Requests

ecified range or
   ranges are appropriate for the entity:

      - The presence of a Range header in an unconditional GET modifies
        what is returned if the GET is otherwise successful. In other
        words, the response carries a status code of 206 (Partial
        Content) instead of 200 (OK).

      - The presence of a Range header in a conditional GET (a request
        using one or both of If-Modified-Since and If-None-Match, or
        one or both of If-Unmodified-Since and If-Match) modifies what
        is returned if the GET is otherwise successful and the
        condition is true. It 
```
</details>

**FAITHFULNESS - TEU_VEREDICTO (fraccao 0-1):** -> 1

---

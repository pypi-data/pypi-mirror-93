# -*- coding: utf-8 -*-

import enum
import six
import attr

from cryptoparser.common.base import Vector, VectorParamNumeric, Serializable
from cryptoparser.common.parse import ParserBinary
from cryptoparser.tls.extension import TlsNamedCurveFactory
from cryptoparser.tls.subprotocol import TlsECCurveType

from .math import is_prime, prime_precheck


@attr.s(eq=False)
class DHParameterNumbers(object):
    p = attr.ib(validator=attr.validators.instance_of(six.integer_types))  # pylint: disable=invalid-name
    g = attr.ib(validator=attr.validators.instance_of(six.integer_types))  # pylint: disable=invalid-name
    q = attr.ib(  # pylint: disable=invalid-name
        default=None, validator=attr.validators.optional(attr.validators.instance_of(six.integer_types))
    )

    def __eq__(self, other):
        return self.p == other.p and self.g == other.g and self.q == other.q


@attr.s
class DHPublicNumbers(object):
    y = attr.ib(validator=attr.validators.instance_of(six.integer_types))  # pylint: disable=invalid-name
    parameter_numbers = attr.ib(validator=attr.validators.instance_of(DHParameterNumbers))


@attr.s
class DHPublicKey(object):
    public_numbers = attr.ib(validator=attr.validators.instance_of(DHPublicNumbers))
    key_size = attr.ib(validator=attr.validators.instance_of(six.integer_types))


@attr.s(eq=False)
class DHParamWellKnown(object):
    dh_param_numbers = attr.ib(validator=attr.validators.instance_of(DHParameterNumbers))
    name = attr.ib(validator=attr.validators.instance_of(six.string_types))
    source = attr.ib(validator=attr.validators.instance_of(six.string_types))
    key_size = attr.ib(validator=attr.validators.instance_of(six.integer_types))

    def __eq__(self, other):
        return self.dh_param_numbers == other.dh_param_numbers


class WellKnownDHParams(enum.Enum):
    RFC3526_1536_BIT_MODP_GROUP = DHParamWellKnown(
        dh_param_numbers=DHParameterNumbers(
            p=int((
                'FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1' +
                '29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD' +
                'EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245' +
                'E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED' +
                'EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D' +
                'C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F' +
                '83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D' +
                '670C354E 4ABC9804 F1746C08 CA237327 FFFFFFFF FFFFFFFF'
            ).replace(' ', ''), 16),
            g=0x2,
        ),
        name='1536-bit MODP Group',
        source='RFC3526',
        key_size=1536,
    )
    RFC3526_2048_BIT_MODP_GROUP = DHParamWellKnown(
        DHParameterNumbers(
            p=int((
                'FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1' +
                '29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD' +
                'EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245' +
                'E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED' +
                'EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D' +
                'C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F' +
                '83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D' +
                '670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B' +
                'E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9' +
                'DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510' +
                '15728E5A 8AACAA68 FFFFFFFF FFFFFFFF'
            ).replace(' ', ''), 16),
            g=0x2,
        ),
        name='2048-bit MODP Group',
        source='RFC3526',
        key_size=2048,
    )
    RFC3526_3072_BIT_MODP_GROUP = DHParamWellKnown(
        DHParameterNumbers(
            p=int((
                'FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1' +
                '29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD' +
                'EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245' +
                'E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED' +
                'EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D' +
                'C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F' +
                '83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D' +
                '670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B' +
                'E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9' +
                'DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510' +
                '15728E5A 8AAAC42D AD33170D 04507A33 A85521AB DF1CBA64' +
                'ECFB8504 58DBEF0A 8AEA7157 5D060C7D B3970F85 A6E1E4C7' +
                'ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226 1AD2EE6B' +
                'F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C' +
                'BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31' +
                '43DB5BFC E0FD108E 4B82D120 A93AD2CA FFFFFFFF FFFFFFFF'
            ).replace(' ', ''), 16),
            g=0x2,
        ),
        name='3072-bit MODP Group',
        source='RFC3526',
        key_size=3072,
    )
    RFC3526_4096_BIT_MODP_GROUP = DHParamWellKnown(
        DHParameterNumbers(
            p=int((
                'FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1' +
                '29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD' +
                'EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245' +
                'E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED' +
                'EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D' +
                'C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F' +
                '83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D' +
                '670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B' +
                'E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9' +
                'DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510' +
                '15728E5A 8AAAC42D AD33170D 04507A33 A85521AB DF1CBA64' +
                'ECFB8504 58DBEF0A 8AEA7157 5D060C7D B3970F85 A6E1E4C7' +
                'ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226 1AD2EE6B' +
                'F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C' +
                'BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31' +
                '43DB5BFC E0FD108E 4B82D120 A9210801 1A723C12 A787E6D7' +
                '88719A10 BDBA5B26 99C32718 6AF4E23C 1A946834 B6150BDA' +
                '2583E9CA 2AD44CE8 DBBBC2DB 04DE8EF9 2E8EFC14 1FBECAA6' +
                '287C5947 4E6BC05D 99B2964F A090C3A2 233BA186 515BE7ED' +
                '1F612970 CEE2D7AF B81BDD76 2170481C D0069127 D5B05AA9' +
                '93B4EA98 8D8FDDC1 86FFB7DC 90A6C08F 4DF435C9 34063199' +
                'FFFFFFFF FFFFFFFF'
            ).replace(' ', ''), 16),
            g=0x2,
        ),
        name='4096-bit MODP Group',
        source='RFC3526',
        key_size=4096,
    )
    RFC3526_6144_BIT_MODP_GROUP = DHParamWellKnown(
        DHParameterNumbers(
            p=int((
                'FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08' +
                '8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B' +
                '302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9' +
                'A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6' +
                '49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8' +
                'FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D' +
                '670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C' +
                '180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718' +
                '3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AAAC42D AD33170D' +
                '04507A33 A85521AB DF1CBA64 ECFB8504 58DBEF0A 8AEA7157 5D060C7D' +
                'B3970F85 A6E1E4C7 ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226' +
                '1AD2EE6B F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C' +
                'BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31 43DB5BFC' +
                'E0FD108E 4B82D120 A9210801 1A723C12 A787E6D7 88719A10 BDBA5B26' +
                '99C32718 6AF4E23C 1A946834 B6150BDA 2583E9CA 2AD44CE8 DBBBC2DB' +
                '04DE8EF9 2E8EFC14 1FBECAA6 287C5947 4E6BC05D 99B2964F A090C3A2' +
                '233BA186 515BE7ED 1F612970 CEE2D7AF B81BDD76 2170481C D0069127' +
                'D5B05AA9 93B4EA98 8D8FDDC1 86FFB7DC 90A6C08F 4DF435C9 34028492' +
                '36C3FAB4 D27C7026 C1D4DCB2 602646DE C9751E76 3DBA37BD F8FF9406' +
                'AD9E530E E5DB382F 413001AE B06A53ED 9027D831 179727B0 865A8918' +
                'DA3EDBEB CF9B14ED 44CE6CBA CED4BB1B DB7F1447 E6CC254B 33205151' +
                '2BD7AF42 6FB8F401 378CD2BF 5983CA01 C64B92EC F032EA15 D1721D03' +
                'F482D7CE 6E74FEF6 D55E702F 46980C82 B5A84031 900B1C9E 59E7C97F' +
                'BEC7E8F3 23A97A7E 36CC88BE 0F1D45B7 FF585AC5 4BD407B2 2B4154AA' +
                'CC8F6D7E BF48E1D8 14CC5ED2 0F8037E0 A79715EE F29BE328 06A1D58B' +
                'B7C5DA76 F550AA3D 8A1FBFF0 EB19CCB1 A313D55C DA56C9EC 2EF29632' +
                '387FE8D7 6E3C0468 043E8F66 3F4860EE 12BF2D5B 0B7474D6 E694F91E' +
                '6DCC4024 FFFFFFFF FFFFFFFF'
            ).replace(' ', ''), 16),
            g=0x2,
        ),
        name='6144-bit MODP Group',
        source='RFC3526',
        key_size=6144,
    )
    RFC3526_8192_BIT_MODP_GROUP = DHParamWellKnown(
        DHParameterNumbers(
            p=int((
                'FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1' +
                '29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD' +
                'EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245' +
                'E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED' +
                'EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D' +
                'C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F' +
                '83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D' +
                '670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B' +
                'E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9' +
                'DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510' +
                '15728E5A 8AAAC42D AD33170D 04507A33 A85521AB DF1CBA64' +
                'ECFB8504 58DBEF0A 8AEA7157 5D060C7D B3970F85 A6E1E4C7' +
                'ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226 1AD2EE6B' +
                'F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C' +
                'BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31' +
                '43DB5BFC E0FD108E 4B82D120 A9210801 1A723C12 A787E6D7' +
                '88719A10 BDBA5B26 99C32718 6AF4E23C 1A946834 B6150BDA' +
                '2583E9CA 2AD44CE8 DBBBC2DB 04DE8EF9 2E8EFC14 1FBECAA6' +
                '287C5947 4E6BC05D 99B2964F A090C3A2 233BA186 515BE7ED' +
                '1F612970 CEE2D7AF B81BDD76 2170481C D0069127 D5B05AA9' +
                '93B4EA98 8D8FDDC1 86FFB7DC 90A6C08F 4DF435C9 34028492' +
                '36C3FAB4 D27C7026 C1D4DCB2 602646DE C9751E76 3DBA37BD' +
                'F8FF9406 AD9E530E E5DB382F 413001AE B06A53ED 9027D831' +
                '179727B0 865A8918 DA3EDBEB CF9B14ED 44CE6CBA CED4BB1B' +
                'DB7F1447 E6CC254B 33205151 2BD7AF42 6FB8F401 378CD2BF' +
                '5983CA01 C64B92EC F032EA15 D1721D03 F482D7CE 6E74FEF6' +
                'D55E702F 46980C82 B5A84031 900B1C9E 59E7C97F BEC7E8F3' +
                '23A97A7E 36CC88BE 0F1D45B7 FF585AC5 4BD407B2 2B4154AA' +
                'CC8F6D7E BF48E1D8 14CC5ED2 0F8037E0 A79715EE F29BE328' +
                '06A1D58B B7C5DA76 F550AA3D 8A1FBFF0 EB19CCB1 A313D55C' +
                'DA56C9EC 2EF29632 387FE8D7 6E3C0468 043E8F66 3F4860EE' +
                '12BF2D5B 0B7474D6 E694F91E 6DBE1159 74A3926F 12FEE5E4' +
                '38777CB6 A932DF8C D8BEC4D0 73B931BA 3BC832B6 8D9DD300' +
                '741FA7BF 8AFC47ED 2576F693 6BA42466 3AAB639C 5AE4F568' +
                '3423B474 2BF1C978 238F16CB E39D652D E3FDB8BE FC848AD9' +
                '22222E04 A4037C07 13EB57A8 1A23F0C7 3473FC64 6CEA306B' +
                '4BCBC886 2F8385DD FA9D4B7F A2C087E8 79683303 ED5BDD3A' +
                '062B3CF5 B3A278A6 6D2A13F8 3F44F82D DF310EE0 74AB6A36' +
                '4597E899 A0255DC1 64F31CC5 0846851D F9AB4819 5DED7EA1' +
                'B1D510BD 7EE74D73 FAF36BC3 1ECFA268 359046F4 EB879F92' +
                '4009438B 481C6CD7 889A002E D5EE382B C9190DA6 FC026E47' +
                '9558E447 5677E9AA 9E3050E2 765694DF C81F56E8 80B96E71' +
                '60C980DD 98EDD3DF FFFFFFFF FFFFFFFF'
            ).replace(' ', ''), 16),
            g=0x2,
        ),
        name='8192-bit MODP Group',
        source='RFC3526',
        key_size=8192,
    )
    RFC5114_1024_BIT_MODP_GROUP_WITH_160_BIT_PRIME_ORDER_SUBGROUP = DHParamWellKnown(  # pylint: disable=invalid-name
        DHParameterNumbers(
            p=int((
                'B10B8F96 A080E01D DE92DE5E AE5D54EC 52C99FBC FB06A3C6' +
                '9A6A9DCA 52D23B61 6073E286 75A23D18 9838EF1E 2EE652C0' +
                '13ECB4AE A9061123 24975C3C D49B83BF ACCBDD7D 90C4BD70' +
                '98488E9C 219A7372 4EFFD6FA E5644738 FAA31A4F F55BCCC0' +
                'A151AF5F 0DC8B4BD 45BF37DF 365C1A65 E68CFDA7 6D4DA708' +
                'DF1FB2BC 2E4A4371'
            ).replace(' ', ''), 16),
            g=int((
                'A4D1CBD5 C3FD3412 6765A442 EFB99905 F8104DD2 58AC507F' +
                'D6406CFF 14266D31 266FEA1E 5C41564B 777E690F 5504F213' +
                '160217B4 B01B886A 5E91547F 9E2749F4 D7FBD7D3 B9A92EE1' +
                '909D0D22 63F80A76 A6A24C08 7A091F53 1DBF0A01 69B6A28A' +
                'D662A4D1 8E73AFA3 2D779D59 18D08BC8 858F4DCE F97C2A24' +
                '855E6EEB 22B3B2E5'
            ).replace(' ', ''), 16),
            q=int((
                'F518AA87 81A8DF27 8ABA4E7D 64B7CB9D 49462353'
            ).replace(' ', ''), 16),
        ),
        name='1024-bit MODP Group with 160-bit Prime Order Subgroup',
        source='RFC5114',
        key_size=1024,
    )
    RFC5114_2048_BIT_MODP_GROUP_WITH_224_BIT_PRIME_ORDER_SUBGROUP = DHParamWellKnown(  # pylint: disable=invalid-name
        DHParameterNumbers(
            p=int((
                'AD107E1E 9123A9D0 D660FAA7 9559C51F A20D64E5 683B9FD1' +
                'B54B1597 B61D0A75 E6FA141D F95A56DB AF9A3C40 7BA1DF15' +
                'EB3D688A 309C180E 1DE6B85A 1274A0A6 6D3F8152 AD6AC212' +
                '9037C9ED EFDA4DF8 D91E8FEF 55B7394B 7AD5B7D0 B6C12207' +
                'C9F98D11 ED34DBF6 C6BA0B2C 8BBC27BE 6A00E0A0 B9C49708' +
                'B3BF8A31 70918836 81286130 BC8985DB 1602E714 415D9330' +
                '278273C7 DE31EFDC 7310F712 1FD5A074 15987D9A DC0A486D' +
                'CDF93ACC 44328387 315D75E1 98C641A4 80CD86A1 B9E587E8' +
                'BE60E69C C928B2B9 C52172E4 13042E9B 23F10B0E 16E79763' +
                'C9B53DCF 4BA80A29 E3FB73C1 6B8E75B9 7EF363E2 FFA31F71' +
                'CF9DE538 4E71B81C 0AC4DFFE 0C10E64F'
            ).replace(' ', ''), 16),
            g=int((
                'AC4032EF 4F2D9AE3 9DF30B5C 8FFDAC50 6CDEBE7B 89998CAF' +
                '74866A08 CFE4FFE3 A6824A4E 10B9A6F0 DD921F01 A70C4AFA' +
                'AB739D77 00C29F52 C57DB17C 620A8652 BE5E9001 A8D66AD7' +
                'C1766910 1999024A F4D02727 5AC1348B B8A762D0 521BC98A' +
                'E2471504 22EA1ED4 09939D54 DA7460CD B5F6C6B2 50717CBE' +
                'F180EB34 118E98D1 19529A45 D6F83456 6E3025E3 16A330EF' +
                'BB77A86F 0C1AB15B 051AE3D4 28C8F8AC B70A8137 150B8EEB' +
                '10E183ED D19963DD D9E263E4 770589EF 6AA21E7F 5F2FF381' +
                'B539CCE3 409D13CD 566AFBB4 8D6C0191 81E1BCFE 94B30269' +
                'EDFE72FE 9B6AA4BD 7B5A0F1C 71CFFF4C 19C418E1 F6EC0179' +
                '81BC087F 2A7065B3 84B890D3 191F2BFA'
            ).replace(' ', ''), 16),
            q=int((
                '801C0D34 C58D93FE 99717710 1F80535A 4738CEBC BF389A99' +
                'B36371EB'
            ).replace(' ', ''), 16),
        ),
        name='2048-bit MODP Group with 224-bit Prime Order Subgroup',
        source='RFC5114',
        key_size=2048,
    )
    RFC5114_2048_BIT_MODP_GROUP_WITH_256_BIT_PRIME_ORDER_SUBGROUP = DHParamWellKnown(  # pylint: disable=invalid-name
        DHParameterNumbers(
            p=int((
                '87A8E61D B4B6663C FFBBD19C 65195999 8CEEF608 660DD0F2' +
                '5D2CEED4 435E3B00 E00DF8F1 D61957D4 FAF7DF45 61B2AA30' +
                '16C3D911 34096FAA 3BF4296D 830E9A7C 209E0C64 97517ABD' +
                '5A8A9D30 6BCF67ED 91F9E672 5B4758C0 22E0B1EF 4275BF7B' +
                '6C5BFC11 D45F9088 B941F54E B1E59BB8 BC39A0BF 12307F5C' +
                '4FDB70C5 81B23F76 B63ACAE1 CAA6B790 2D525267 35488A0E' +
                'F13C6D9A 51BFA4AB 3AD83477 96524D8E F6A167B5 A41825D9' +
                '67E144E5 14056425 1CCACB83 E6B486F6 B3CA3F79 71506026' +
                'C0B857F6 89962856 DED4010A BD0BE621 C3A3960A 54E710C3' +
                '75F26375 D7014103 A4B54330 C198AF12 6116D227 6E11715F' +
                '693877FA D7EF09CA DB094AE9 1E1A1597'
            ).replace(' ', ''), 16),
            g=int((
                '3FB32C9B 73134D0B 2E775066 60EDBD48 4CA7B18F 21EF2054' +
                '07F4793A 1A0BA125 10DBC150 77BE463F FF4FED4A AC0BB555' +
                'BE3A6C1B 0C6B47B1 BC3773BF 7E8C6F62 901228F8 C28CBB18' +
                'A55AE313 41000A65 0196F931 C77A57F2 DDF463E5 E9EC144B' +
                '777DE62A AAB8A862 8AC376D2 82D6ED38 64E67982 428EBC83' +
                '1D14348F 6F2F9193 B5045AF2 767164E1 DFC967C1 FB3F2E55' +
                'A4BD1BFF E83B9C80 D052B985 D182EA0A DB2A3B73 13D3FE14' +
                'C8484B1E 052588B9 B7D2BBD2 DF016199 ECD06E15 57CD0915' +
                'B3353BBB 64E0EC37 7FD02837 0DF92B52 C7891428 CDC67EB6' +
                '184B523D 1DB246C3 2F630784 90F00EF8 D647D148 D4795451' +
                '5E2327CF EF98C582 664B4C0F 6CC41659'
            ).replace(' ', ''), 16),
            q=int((
                '8CF83642 A709A097 B4479976 40129DA2 99B1A47D 1EB3750B' +
                'A308B0FE 64F5FBD3'
            ).replace(' ', ''), 16),
        ),
        name='2048-bit MODP Group with 256-bit Prime Order Subgroup',
        source='RFC5114',
        key_size=2048,
    )


class TlsDHParamVector(Vector):  # pylint: disable=too-many-ancestors
    @classmethod
    def get_param(cls):
        return VectorParamNumeric(item_size=1, min_byte_num=1, max_byte_num=2 ** 16 - 1)


def parse_dh_params(param_bytes):
    parser = ParserBinary(param_bytes)

    parser.parse_parsable('p', TlsDHParamVector)
    parser.parse_parsable('g', TlsDHParamVector)
    parser.parse_parsable('y', TlsDHParamVector)

    p = int(''.join(map('{:02x}'.format, parser['p'])), 16)  # pylint: disable=invalid-name
    g = int(''.join(map('{:02x}'.format, parser['g'])), 16)  # pylint: disable=invalid-name
    y = int(''.join(map('{:02x}'.format, parser['y'])), 16)  # pylint: disable=invalid-name

    parameter_numbers = DHParameterNumbers(p, g)
    public_numbers = DHPublicNumbers(y, parameter_numbers)

    return DHPublicKey(public_numbers, len(parser['p']) * 8)


def parse_ecdh_params(param_bytes):
    parser = ParserBinary(param_bytes)

    parser.parse_numeric('curve_type', 1, TlsECCurveType)

    if parser['curve_type'] != TlsECCurveType.NAMED_CURVE:
        raise NotImplementedError(parser['curve_type'])

    parser.parse_parsable('named_curve', TlsNamedCurveFactory)

    parser.parse_numeric('public_key_length', 1)
    parser.parse_bytes('public_key', parser['public_key_length'])

    return parser['named_curve'], parser['public_key']


@attr.s
class DHParameter(Serializable):
    public_key = attr.ib(validator=attr.validators.instance_of(DHPublicKey))
    reused = attr.ib(validator=attr.validators.instance_of(bool))
    well_known = attr.ib(init=False, validator=attr.validators.instance_of(bool))
    prime = attr.ib(init=False, validator=attr.validators.instance_of(bool))
    safe_prime = attr.ib(init=False, validator=attr.validators.instance_of(bool))

    def _check_prime(self):
        param_num_p = self.public_key.public_numbers.parameter_numbers.p
        param_num_g = self.public_key.public_numbers.parameter_numbers.g

        self.prime, self.safe_prime = prime_precheck(param_num_p, param_num_g)

        # If the number is not divisible by any of the small primes, then
        # move on to the full Miller-Rabin test.
        self.prime = is_prime(self.key_size, param_num_p)
        if self.prime:
            self.safe_prime = is_prime(self.key_size, param_num_p // 2)

    def __attrs_post_init__(self):
        for well_know_public_number in WellKnownDHParams:
            if well_know_public_number.value.dh_param_numbers == self.public_key.public_numbers.parameter_numbers:
                self.well_known = well_know_public_number
                self.prime = True
                self.safe_prime = True
                break
        else:
            self.well_known = None
            self._check_prime()

    @property
    def key_size(self):
        return self.public_key.key_size

    def _asdict(self):
        result = {'key_size': self.key_size}
        result.update({
            key: value
            for key, value in self.__dict__.items()
            if key != 'public_key'
        })
        return result

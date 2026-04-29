# -*- coding: utf-8 -*-

import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent

# source_name refers to the file in OUTPUT_DIR downloaded by "Update lazy rules"
RULE_VARIANTS = [
    ('lazy.conf',          'lazy.conf',       False),
    ('lazy_ad.conf',       'lazy.conf',       True),
    ('lazy_group.conf',    'lazy_group.conf', False),
    ('lazy_group_ad.conf', 'lazy_group.conf', True),
]

RULE_PREFIX_PATTERN = re.compile(
    r'^(DOMAIN-SUFFIX|DOMAIN-KEYWORD|DOMAIN|USER-AGENT|URL-REGEX|IP-CIDR|IP-ASN|RULE-SET|DOMAIN-SET|SCRIPT|DST-PORT|GEOIP|FINAL|AND|NOT|OR),',
    re.IGNORECASE,
)


def get_rules_string_from_file(path, kind):
    contents = path.read_text(encoding='utf-8').splitlines()
    ret = ''

    for content in contents:
        content = content.strip('\r\n')
        if not len(content):
            continue

        if content.startswith('#'):
            ret += content + '\n'
            continue

        prefix = 'DOMAIN-SUFFIX'
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', content):
            prefix = 'IP-CIDR'
            if '/' not in content:
                content += '/32'
        elif re.match(r'((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?', content):
            prefix = 'IP-CIDR'
            if '/' not in content:
                content += '/128'
        elif '.' not in content and len(content) > 1:
            prefix = 'DOMAIN-KEYWORD'

        ret += '%s,%s,%s\n' % (prefix, content, kind)

    return ret


def read_custom_rules():
    content = (BASE_DIR / 'custom_rules.conf').read_text(encoding='utf-8')
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if stripped.startswith('[') and stripped.endswith(']'):
            raise ValueError('custom_rules.conf must not contain section headers')
        if stripped.upper().startswith('FINAL,'):
            raise ValueError('custom_rules.conf must not contain FINAL rules')
        if not RULE_PREFIX_PATTERN.match(stripped):
            raise ValueError('custom_rules.conf contains unsupported rule syntax: %s' % stripped)
    return content.strip()


def has_active_rules(content):
    return any(
        line.strip() and not line.strip().startswith('#')
        for line in content.splitlines()
    )


def build_managed_block(custom_rules, with_ads):
    parts = []

    if custom_rules and has_active_rules(custom_rules):
        parts.append('# Managed custom rules')
        parts.append(custom_rules)

    if with_ads:
        ad_rules = (
            get_rules_string_from_file(BASE_DIR / 'manual_reject.txt', 'REJECT')
            + get_rules_string_from_file(BASE_DIR / 'resultant/ad.list', 'REJECT')
        ).strip()
        if has_active_rules(ad_rules):
            parts.append('# Managed ad block rules')
            parts.append(ad_rules)

    if not parts:
        return ''

    return '\n\n'.join(parts) + '\n\n'


def inject_rule_block(config_text, managed_block):
    if not managed_block:
        return config_text

    lines = config_text.splitlines()
    rule_index = None
    insert_index = None

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '[Rule]':
            rule_index = index
            continue

        if rule_index is None:
            continue

        if stripped.startswith('[') and stripped.endswith(']'):
            if insert_index is None:
                insert_index = index
            break

        if stripped and not stripped.startswith('#'):
            insert_index = index
            break

    if rule_index is None:
        raise ValueError('Missing [Rule] section in lazy template')

    if insert_index is None:
        insert_index = len(lines)

    managed_lines = managed_block.rstrip('\n').splitlines()
    new_lines = lines[:insert_index] + managed_lines + [''] + lines[insert_index:]
    return '\n'.join(new_lines) + '\n'


def normalize_output(config_text):
    return re.sub(r'\n{3,}', '\n\n', config_text).rstrip() + '\n'


def main():
    custom_rules = read_custom_rules()

    # Read source files before any writes to avoid reading already-modified content
    source_cache = {}
    for _, source_name, _ in RULE_VARIANTS:
        if source_name not in source_cache:
            source_cache[source_name] = (OUTPUT_DIR / source_name).read_text(encoding='utf-8')

    for output_name, source_name, with_ads in RULE_VARIANTS:
        config_text = source_cache[source_name]
        managed_block = build_managed_block(custom_rules, with_ads)
        output_text = normalize_output(inject_rule_block(config_text, managed_block))
        (OUTPUT_DIR / output_name).write_text(output_text, encoding='utf-8')


if __name__ == '__main__':
    main()
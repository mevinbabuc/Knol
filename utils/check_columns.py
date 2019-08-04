import pandas as pd

known = {'append_source', 'available_price', 'block_count', 'block_error', 'blocksExtracted', 'brand',
         'bytes_transfered', 'country', 'crawl_date', 'crawl_time', 'crawl_type', 'created_time', 'dump_files',
         'encoding_temp', 'error', 'ext_method', 'ext_time', 'ext_time_elapsed', 'failed_field_ids', 'http_status',
         'ip_address', 'job_id', 'job_root', 'kafka_topic', 'machine_address', 'machine_name', 'meta', 'mrp',
         'no_ratings', 'offer_description', 'online_fn_error', 'original_http_status', 'page_error', 'pagination_url',
         'pagination_urlh', 'param_url', 'parent_id', 'rank', 'rgf_trac_conf', 'seed_url', 'seed_urlh', 'sk', 'sku_s',
         'source', 'source_type', 'thumbnail', 'time_elapsed', 'title', 'tracking_code', 'url', 'urlh', 'vertical',
         'zip'}

chunks = pd.read_json('20190801_20190801_1_bestbuy-us_listing', lines=True, chunksize=10000)

for each in chunks:
    column_set = set(each.columns)

    foo = known.difference(column_set)
    print(foo)

######### ---------------------


cols = ['warranty', 'available_price', 'last_available_price', 'subcategory', 'color', 'sale', 'title', 'specification', 'category', 'shipping_charges', 'description', 'model_no', 'product_description_html', 'no_reviews', 'meta', 'url', 'thumbnail', "stock"]


import pandas as pd
df = pd.read_json('20190801_20190801_1_newegg-us_listing.gz', lines=True, compression='gzip')

data = df[df.specification.notnull()][cols]

# frozen_string_literal: true

# Strip query parameters from image URLs in post content
# This fixes issues with WordPress-imported images that have query params like ?w=300
module Jekyll
  module StripImageQueryParams
    # Strip query parameters from img src attributes
    def strip_img_query_params(content)
      return content unless content
      
      # Match img tags with src attributes that have query parameters
      content.gsub(/<img([^>]*?)src="([^"]+?)\?[^"]*"([^>]*?)>/i) do |match|
        before_src = $1
        url_without_query = $2
        after_src = $3
        "<img#{before_src}src=\"#{url_without_query}\"#{after_src}>"
      end
    end
  end
  
  class StripImageQueryParamsGenerator < Generator
    priority :low
    
    def generate(site)
      site.posts.docs.each do |post|
        if post.content
          post.content = strip_content(post.content)
        end
      end
    end
    
    private
    
    def strip_content(content)
      # Match img tags with src attributes that have query parameters
      content.gsub(/<img([^>]*?)src="([^"]+?)\?[^"]*"([^>]*?)>/i) do |match|
        before_src = $1
        url_without_query = $2
        after_src = $3
        "<img#{before_src}src=\"#{url_without_query}\"#{after_src}>"
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::StripImageQueryParams)

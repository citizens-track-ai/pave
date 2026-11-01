# frozen_string_literal: true

module Jekyll
  class CasePrintGenerator < Generator
    safe true
    priority :low

    def generate(site)
      return unless site.collections.key?('cases')

      site.collections['cases'].docs.each do |doc|
        site.pages << CasePrintPage.new(site, doc)
      end
    end
  end

  class CasePrintPage < Page
    def initialize(site, doc)
      @site = site
      @base = site.source
      @dir  = 'cases'
      slug  = doc.data['slug'] || File.basename(doc.basename_without_ext)
      @name = "#{slug}-print.html"

      self.process(@name)

      # Inherit all fields from parent case document
      self.data = doc.data.dup

      # Print-specific SEO and routing overrides
      self.data['layout'] = 'case_print'
      self.data['sitemap'] = false
      self.data['robots'] = 'noindex, nofollow, noarchive'
      self.data['canonical_url'] = doc.url
      self.data['permalink'] = "/cases/#{slug}-print.html"
      self.data['is_print_view'] = true

      self.content = ''
    end
  end
end

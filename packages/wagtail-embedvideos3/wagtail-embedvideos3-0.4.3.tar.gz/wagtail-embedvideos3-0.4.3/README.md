# ABANDONED, BUT STILL SUPPORT Wagtail >= 2.2 Django >= 2.0 <= 3.1


With the introduction of Embedded Content in wagtail 1.12 [https://docs.wagtail.io/en/v1.12.6/releases/1.12.html#improved-embed-configuration](https://docs.wagtail.io/en/v1.12.6/releases/1.12.html#improved-embed-configuration), this package will no longer be needed in new projects. It`s for some old projects, that still use this package.

# WAGTAIL EMBED VIDEOS

Simple app that works similar to wagtailimages, but for embedding YouTube and Vimeo videos and music from SoundCloud.
It's an integration of [django-embed-video](https://github.com/yetty/django-embed-video)


## WARNING

With recent changes to keep up with Wagtail current versions, we do **not** support versions < 2.2!

Latest version only suports django >= 2.0 and wagtail >= 2.2


## Quick start

1. Add "embed_video" and "wagtail_embed_videos" to your INSTALLED_APPS setting like this:

        INSTALLED_APPS = (
            ...
            'embed_video',
            'wagtail_embed_videos',
            ...
        )

2. Run `python manage.py makemigrations` to create the migration for wagtail_embed_videos models

3. Run `python manage.py migrate` to create the models of wagtail_embed_videos app

4. Using wagtail_embed_videos:

        from wagtail_embed_videos.edit_handlers import EmbedVideoChooserPanel

        class VideoBasedModel(models.Model):
            video = models.ForeignKey(
                'wagtail_embed_videos.EmbedVideo',
                verbose_name="Video",
                null=True,
                blank=True,
                on_delete=models.SET_NULL,
                related_name='+'
            )
            ...
            content_panels = [EmbedVideoChooserPanel('video')] 
        
        # maybe in some older versions of Wagtail you need replace 'content_panels' with 'panels'
        # accessing the EmbedVideoField() in the model 'wagtail_embed_videos.EmbedVideo'
        # this is the field used for storing the url of the embed video
        video_based_model_instanse.video.url

        # accessing the thumbnail image in the model 'wagtailimages'
        # this is a foreign key to model Image
        video_based_model_instanse.video.thumbnail

5. For render your video in a template put `{% load embed_video_tags%}` for load template tags and put this code where you want render your video:

        ```html
        {% video VideoBasedModel.video.url as video %}
                {% video video 'small' %}
        {% endvideo %}
        ```

6. Check [django-embed-video](https://github.com/yetty/django-embed-video) for more documentation


## Release Notes

### v0.4.3

 - Wagtail version >= 2.2 supported up to version == 2.11.3;
 - Django version >= 3.0 supported (Django >= 3.1 was not tested);
 - Fix for modal workflow change introduced in Wagtail 2.2


### v0.4.1

 - Wagtail version >= 2.0 supported;
 - Django version >= 2.0 supported;
 - Dropped support for Wagtail < 2.0;

### v0.3.0

 - Changed the structure of "AbstractEmbedVideo", because "TagSearchable" is not used anymore;

### v0.2.5

 - This is the last version compatible with Wagtail <= 1.6, because TagSearchable was deprecated and then removed.
